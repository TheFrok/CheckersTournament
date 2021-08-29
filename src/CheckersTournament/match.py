import random
from typing import List, Type

from game import GameMechanics
from game_elements.board import Board, Move
from game_elements.piece import PlayerId
from strategies import Strategy, ALL_STRATEGIES


class Player:
    def __init__(self, player_id: int, strategy: Type[Strategy]):
        self.player_id = player_id
        self.strategy = strategy(player_id)

    def play_turn(self, board: Board, legal_moves: List[List[Move]]):
        best_move = self.strategy.choose_best_move(board, legal_moves)
        board.run_moves(best_move)

    def get_player_id(self) -> int:
        return self.player_id


class Match:
    def __init__(self, players: List[Player], board: Board):
        self.players = players
        self.board = board
        self.current_player_index = None

    def is_win(self):
        for i in self.players:
            pieces = self.board.get_player_pieces_location(i.get_player_id())
            if len(pieces) == 0:
                return True
        return False

    def setup_match(self):
        self.board.reset()
        self.current_player_index = 0

    def get_legal_moves_for_player(self, player: Player = None) -> List[List[Move]]:
        if player is None:
            player = self.players[self.current_player_index]
        return GameMechanics.get_player_legal_moves(self.board, player.player_id)

    def match(self):
        self.setup_match()
        is_over = False
        legal_moves = self.get_legal_moves_for_player()
        while not is_over:
            self.play_once(legal_moves)
            self.set_next_player()
            legal_moves = self.get_legal_moves_for_player()
            is_over = self.is_win() or len(legal_moves) == 0
        # print(f"Player {(self.current_player_index -1) % len(self.players)} won:")
        # print(self.board)
        return self.current_player_index

    def play_once(self, legal_moves: List[List[Move]]):
        player = self.players[self.current_player_index]
        player.play_turn(self.board, legal_moves)

    def set_next_player(self):
        self.current_player_index += 1
        self.current_player_index %= len(self.players)
        self.board.rotate()


def play_match():
    strat1 = random.choice(ALL_STRATEGIES)
    strat2 = random.choice(ALL_STRATEGIES)
    player1 = Player(PlayerId.white.value, strat1)
    player2 = Player(PlayerId.black.value, strat2)
    board = Board()
    players = [player1, player2]
    match = Match(players, board)
    i = match.match()
    print(f'player {i} wins with strategy {players[i].strategy.__class__}\n'
          f'other staretegy was: {players[i^1].strategy.__class__}')
