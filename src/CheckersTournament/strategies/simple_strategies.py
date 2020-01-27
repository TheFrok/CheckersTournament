import random
from math import sqrt
from statistics import mean

from .base_strategy import Strategy


class RandomStrategy(Strategy):
    def choose_best_move(self, board, legal_moves):
        return random.choice(legal_moves)


class LongestLineStrategy(Strategy):
    def rank_move(self, board, move, **kwargs):
        return len(move)


class StayBack(Strategy):
    def rank_move(self, board, move, **kwargs):
        start, end = self._get_start_end_squares(move)
        diff = start.row - end.row
        return (start.row + 1) ** diff


class PushForward(StayBack):
    def rank_move(self, board, move, **kwargs):
        stay_back_rank = super().rank_move(board, move)
        return - stay_back_rank


class TowardEnemyCenter(Strategy):
    def rank_move(self, board, move, **board_data):
        start, end = self._get_start_end_squares(move)
        col_d = end.col - board_data['col']
        row_d = end.col - board_data['row']
        return sqrt(row_d**2 + col_d**2)

    def analyze_board(self, board):
        other_player = (self.player_id + 1) % 2
        enemy_location = board.player_pieces[other_player]
        avg_col = mean([sqr.col for sqr in enemy_location])
        avg_row = mean([sqr.row for sqr in enemy_location])
        return dict(row=avg_row, col=avg_col)
