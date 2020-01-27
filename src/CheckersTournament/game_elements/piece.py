from enum import Enum


class PlayerId(Enum):
    white = 0
    black = 1
    null = -1


class PieceType(Enum):
    illegal = -1
    empty = 0
    man = 1
    king = 2

    EMPTY_STR = '   '
    ILLEGAL_STR = '@@@'

    @classmethod
    def from_str(cls, str_piece: str):
        if str_piece == cls.EMPTY_STR.value:
            return cls.empty, PlayerId.null
        if str_piece == cls.ILLEGAL_STR.value:
            return cls.illegal, PlayerId.null
        else:
            value, player_id = str_piece.split(',')
            value = cls.man if value == '1' else cls.king
            return value, int(player_id)

    def to_str(self, player_id: int):
        if self == self.empty:
            return self.EMPTY_STR.value
        if self == self.illegal:
            return self.ILLEGAL_STR.value
        assert player_id >= 0
        return f'{self.value},{player_id}'

    def valid_movement_direction(self, board_orientation: int) -> tuple:
        forward = 1 * board_orientation
        backward = -1 * board_orientation
        if self.name == 'man':
            return (forward, )
        if self.name == 'king':
            return (forward, backward)
        return tuple()
