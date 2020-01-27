from typing import List, Tuple

from .game_elements.board import Board, Vector, Square, Move
from .game_elements.piece import PieceType


class GameMechanics:
    DIRECTION_VECTORS = tuple(Vector(*v) for v in (
        (-1, 1), (0, 1), (1, 1),
        (-1, 0),         (1, 0),
        (-1,-1), (0,-1), (1,-1),
    ))

    @classmethod
    def get_player_legal_moves(cls, board: Board, player_id: int) -> List[List[Move]]:
        steps = []
        captures = []
        for square in board.get_player_pieces_location(player_id):
            piece_captures, piece_steps = cls.get_piece_legal_moves(board, square)
            steps += piece_steps
            captures += piece_captures
        if captures:
            return captures
        return steps

    @classmethod
    def get_piece_legal_moves(cls, board: Board, square: Square) -> Tuple[List[List[Move]], List[List[Move]]]:
        assert not board.is_empty(square)
        captures = cls.get_valid_captures(board, square)
        valid_moves = cls.get_piece_legal_steps(board, square)
        return captures, valid_moves

    @classmethod
    def validate_movement_vector(cls, board: Board, square: Square, vector: Vector) -> bool:
        piece, player_id = board.get_location(square)
        new_square = square + vector
        if not board.is_valid_square(new_square):
            return False
        assert isinstance(piece, PieceType)
        if vector.row not in piece.valid_movement_direction(board.orientation):
            return False
        return True

    @classmethod
    def validate_capture_squares(cls, board: Board, start_sqr: Square, first_step: Square, second_step: Square):
        if not board.is_valid_square(first_step):
            return False
        if board.is_empty(first_step):
            return False
        _, player_id = board.get_location(start_sqr)
        _, new_location_player_id = board.get_location(first_step)
        if player_id == new_location_player_id:
            return False
        return board.is_valid_square(second_step) and board.is_empty(second_step)

    @classmethod
    def get_valid_captures(cls, board: Board, square: Square, all_direction: bool = False) -> List[List[Move]]:
        valid_captures = []
        for vector in cls.DIRECTION_VECTORS:
            if not (all_direction or cls.validate_movement_vector(board, square, vector)):
                continue
            if 0 in vector:
                continue
            captures = cls.get_valid_captures_in_vector(board, square, vector)
            if captures:
                new_board = Board.duplicate(board)
                last_square = new_board.run_moves(captures)
                next_captures = cls.get_valid_captures(new_board, last_square, all_direction=True)
                if next_captures:
                    lines = []
                    for line in next_captures:
                        lines.append(captures + line)
                    captures = lines
                else:
                    captures = [captures]
                valid_captures += captures
        return valid_captures

    @classmethod
    def get_valid_captures_in_vector(cls, board: Board, square: Square, vector: Vector) -> List[Move]:
        first_step = square + vector
        second_step = first_step + vector
        if not cls.validate_capture_squares(board, square, first_step, second_step):
            return []
        moves = [Move(square, first_step),
                 Move(first_step, second_step)]
        return moves

    @classmethod
    def get_piece_legal_steps(cls, board: Board, square: Square) -> List[List[Move]]:
        legal_steps = []
        for vector in cls.DIRECTION_VECTORS:
            if 0 in vector:
                continue
            if cls.check_step_in_vector(board, square, vector):
                legal_steps.append([Move(square, square + vector)])
        return legal_steps

    @classmethod
    def check_step_in_vector(cls, board: Board, square: Square, vector: Vector) -> bool:
        if not cls.validate_movement_vector(board, square, vector):
            return False
        new_square = square + vector
        if board.is_empty(new_square):
            return True
        else:
            return False
