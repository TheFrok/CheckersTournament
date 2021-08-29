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
        return best_move

    def get_player_id(self) -> int:
        return self.player_id


class Match:
    def __init__(self, players: List[Player], board: Board):
        self.players: List[Player] = players
        self.board: Board = board
        self.last_move: Move = None
        self.moves_count: int = 0
        self.current_player_index: int = None

    def get_state_str(self):
        b = str(self.board).splitlines()
        last_move = f"The last move that was played was {self.last_move}"
        cur_player = f"The current player is {self.current_player_index}"
        b[4] = b[4] + "\t" + last_move
        b[5] = b[5] + "\t" + cur_player
        return f"Board after move {self.moves_count}\n" + "\n".join(b)

    def is_win(self):
        for p in self.players:
            pieces = self.board.get_player_pieces_location(p.get_player_id())
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
        return self.get_previous_player()

    def play_once(self, legal_moves: List[List[Move]]):
        player = self.players[self.current_player_index]
        played_move = player.play_turn(self.board, legal_moves)
        self.last_move = played_move
        self.moves_count += 1
        return played_move

    def set_next_player(self):
        self.current_player_index += 1
        self.current_player_index %= len(self.players)
        self.board.rotate()

    def debug_match(self):
        self.setup_match()
        is_over = False
        legal_moves = self.get_legal_moves_for_player()
        while not is_over:
            input("Press any key for next move...")
            print(self.get_state_str())
            played_move = self.play_once(legal_moves)
            self.set_next_player()
            legal_moves = self.get_legal_moves_for_player()
            is_over = self.is_win() or len(legal_moves) == 0
        return self.get_previous_player()

    def get_previous_player(self):
        return (self.current_player_index - 1) % len(self.players)


def play_match():
    strat1 = random.choice(ALL_STRATEGIES)
    strat2 = random.choice(ALL_STRATEGIES)
    player1 = Player(PlayerId.white.value, strat1)
    player2 = Player(PlayerId.black.value, strat2)
    board = Board()
    players = [player1, player2]
    match = Match(players, board)
    winner_id = match.match()
    print(match.get_state_str())
    print(f'player {winner_id} wins with strategy {players[winner_id].strategy.__class__}\n'
          f'other staretegy was: {players[winner_id^1].strategy.__class__}')

if __name__ =="__main__":
    play_match()