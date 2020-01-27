from collections import namedtuple
from typing import Tuple, List

from .piece import PieceType, PlayerId

Vector = namedtuple('Vector', 'row col')
Move = namedtuple('Move', 'from_square to_square')


class Square:
    @classmethod
    def tuple_to_square(cls, tup):
        assert len(tup) == 2
        return Square(row=tup[0], col=tup[1])

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __lt__(self, other):
        s1 = self.row, self.col
        s2 = other.row, other.col
        return s1 < s2

    def __add__(self, other: Vector):
        assert isinstance(other, Vector), f'expected {Vector} found {other.__class__}'
        return Square(self.row + other.row, self.col + other.col)

    def __repr__(self):
        return f'Square({self.row},{self.col})'


class Board:
    MAX_ROW = 8
    MAX_COL = 8
    NULL_PLAYER = PlayerId.null.value
    WHITE = PlayerId.white.value
    BLACK = PlayerId.black.value

    @classmethod
    def get_new_board(cls):
        board = list()
        piece_location = dict({cls.WHITE: list(), cls.BLACK: list()})
        for row in range(cls.MAX_ROW):
            board.append([None] * cls.MAX_COL)
            for col in range(cls.MAX_COL):
                if (col + row) % 2 == 1:
                    board[row][col] = (PieceType.illegal, cls.NULL_PLAYER)
                elif row <= 2:
                    board[row][col] = (PieceType.man, cls.WHITE)
                    piece_location[cls.WHITE].append(Square(row, col))
                elif row >= 5:
                    board[row][col] = (PieceType.man, cls.BLACK)
                    piece_location[cls.BLACK].append(Square(row, col))
                else:
                    board[row][col] = (PieceType.empty, cls.NULL_PLAYER)
        return board, piece_location

    @classmethod
    def get_empty_board(cls):
        board = []
        piece_location = {cls.WHITE: [], cls.BLACK: []}
        for row in range(cls.MAX_ROW):
            board.append([None] * cls.MAX_COL)
            for col in range(cls.MAX_COL):
                if (col + row) % 2 == 1:
                    board[row][col] = (PieceType.illegal, cls.NULL_PLAYER)
                else:
                    board[row][col] = (PieceType.empty, cls.NULL_PLAYER)
        return board, piece_location

    @classmethod
    def load_from_str(cls, str_board: str):
        new_board = Board(empty=True)
        lines = [line for line in str_board.splitlines()
                 if not line.startswith('-')]
        for row in range(cls.MAX_ROW):
            pieces = [piece_str for piece_str in lines[row].split('|')
                      if len(piece_str) > 0]
            for col in range(cls.MAX_COL):
                if ',' in pieces[col]:
                    piece, player_id = PieceType.from_str(pieces[col])
                    sqr = Square(row, col)
                    new_board.set_location(sqr, piece, player_id)
        return new_board

    @classmethod
    def duplicate(cls, board):
        assert isinstance(board, cls)
        new = Board(empty=True)
        for player, pieces_list in board.player_pieces.items():
            for square in pieces_list:
                pt, _ = board.get_location(square)
                new.set_location(square, pt, player)
        return new

    def __init__(self, empty: bool =False):
        if empty:
            self._board, self.player_pieces = self.get_empty_board()
        else:
            self._board, self.player_pieces = self.get_new_board()
        self.orientation = 1

    def __str__(self):
        sep = '-' * (8*4 + 1)
        lines = [sep]
        for line in self._board:
            str_line = [piece.to_str(player) for piece, player in line]
            lines += [f'|{"|".join(str_line)}|']
            lines += [sep]
        return '\n'.join(lines)

    def reset(self):
        self._board, self.player_pieces = self.get_new_board()
        self.orientation = 1

    def get_dims(self):
        return self.MAX_ROW, self.MAX_COL

    def set_location(self, square: Square, piece_type: PieceType, player_id: int):
        _, cur_player_id = self.get_location(square)
        if cur_player_id in self.player_pieces.keys():
            self.player_pieces[cur_player_id].remove(square)
        self._board[square.row][square.col] = (piece_type, player_id)
        if player_id in self.player_pieces.keys():
            self.player_pieces[player_id].append(square)

    def get_location(self, square: Square) -> Tuple:
        assert self.is_valid_square(square)
        piece = self._board[square.row][square.col]
        return piece

    def is_empty(self, square: Square):
        piece_type = self.get_location(square)[0]
        return piece_type.value == PieceType.empty.value

    def is_valid_square(self, square: Square) -> bool:
        if square.row >= self.MAX_ROW or square.col >= self.MAX_COL:
            return False
        if square.row < 0 or square.col < 0:
            return False
        return True

    def rotate(self):
        self.orientation *= -1

    def move(self, move: Move):
        assert self.is_valid_square(move.to_square) and self.is_valid_square(move.from_square)
        piece_type, player = self.get_location(move.from_square)
        # Crown a man when reaching last row
        if move.to_square.row in (0, self.MAX_ROW-1):
            piece_type = PieceType.king
        self.set_location(move.to_square, piece_type, player)
        self.set_location(move.from_square, PieceType.empty, self.NULL_PLAYER)
        return move.to_square

    def run_moves(self, move_list: List[Move]):
        if len(move_list) == 0:
            return None
        for move in move_list:
            self.move(move)
        return move.to_square

    def get_player_pieces_location(self, player_id) -> List:
        return self.player_pieces[player_id]


if __name__ == '__main__':
    print(Board())
