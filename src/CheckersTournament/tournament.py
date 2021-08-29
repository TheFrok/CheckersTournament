from game_elements.board import Board

from game_elements.piece import PlayerId
from match import Player, Match
from strategies import ALL_STRATEGIES

NUM_OF_GAMES = 50


class Tournament:
    @staticmethod
    def run_tournament():
        len_strat = len(ALL_STRATEGIES)
        result = []
        board = Board()
        for i in range(len_strat):
            line_result = []
            for j in range(len_strat):
                if i == j:
                    line_result.append(-1)
                    continue
                player1 = Player(PlayerId.white.value, ALL_STRATEGIES[i])
                player2 = Player(PlayerId.black.value, ALL_STRATEGIES[j])
                match = Match([player1, player2], board)
                black_wins = 0
                print(f'Matching {player1.strategy.__class__.__name__} as white\n'
                      f'     VS. {player2.strategy.__class__.__name__} as black')
                for games in range(NUM_OF_GAMES):
                    black_wins += match.match()
                line_result.append(black_wins/NUM_OF_GAMES)
                print(f'White won {(NUM_OF_GAMES - black_wins)/NUM_OF_GAMES*100}%')
            result.append(line_result)
        print(list(map(lambda x: x.__name__, ALL_STRATEGIES)))
        print('\n'.join([str(l) for l in result]))
