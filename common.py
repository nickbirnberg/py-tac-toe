from enum import IntEnum, Enum


class GamePiece(IntEnum):
    blank = 0
    X = 1
    O = 2


class GameMessages(IntEnum):
    WINNER = 0
    LOSER = 1
    DRAW = 2
    MAKE_MOVE = 3
