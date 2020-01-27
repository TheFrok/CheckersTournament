from .base_strategy import Strategy
from .simple_strategies import StayBack, RandomStrategy, LongestLineStrategy, PushForward, \
    TowardEnemyCenter

ALL_STRATEGIES = [RandomStrategy,
                  # StayBack,
                  # PushForward,
                  LongestLineStrategy,
                  TowardEnemyCenter]
