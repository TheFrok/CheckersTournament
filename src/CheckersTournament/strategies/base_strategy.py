import random
from typing import List
from collections import defaultdict

from game_elements.board import Move, Board, Square


class Strategy:
    def __init__(self, player_id=None, **kwargs):
        self.player_id = player_id
        self.other_params = kwargs

    @staticmethod
    def _get_start_end_squares(move: List[Move]) -> (Square, Square):
        starting_position = move[0].from_square
        ending_position = move[-1].to_square
        return starting_position, ending_position

    def rank_move(self, board: Board, move: List[Move], **kwargs) -> float:
        raise NotImplementedError

    def analyze_board(self, board: Board) -> dict:
        pass

    def choose_best_move(self, board: Board, legal_moves: List[List[Move]]) -> List[Move]:
        d = defaultdict(list)
        board_data = self.analyze_board(board) or dict()
        for line in legal_moves:
            d[self.rank_move(board, line, **board_data)].append(line)
        best_rank = max(d.keys())
        return random.choice(d[best_rank])


