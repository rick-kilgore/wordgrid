
from enum import Enum
from typing import Dict


BLANK: str = "__"
DL: str = "DL"
TL: str = "TL"
DW: str = "DW"
TW: str = "TW"

GWIDTH: int = 15
GHEIGHT: int = 15


MULT_SQUARES: Dict[int, str] = {
  3: TW, 6: TL, 8: TL, 11: TW,
  17: DL, 20: DW, 24: DW, 27: DL,
  31: DL, 34: DL, 40: DL, 43: DL,
  45: TW, 48: TL, 52: DW, 56: TL, 59: TW,
  62: DL, 66: DL, 68: DL, 72: DL,
  76: DW, 80: TL, 84: TL, 88: DW,
  90: TL, 94: DL, 100: DL, 104: TL,
  108: DW, 116: DW,
}


class Dir(Enum):
  UP = 1
  RIGHT = 2
  DOWN = 3
  LEFT = 4


def opposite(dirn: Dir) -> Dir:
  match dirn:
    case Dir.UP:
      return Dir.DOWN
    case Dir.DOWN:
      return Dir.UP
    case Dir.LEFT:
      return Dir.RIGHT
    case Dir.RIGHT:
      return Dir.LEFT
  raise Exception(f"unrecognized direction: {dirn}")

LETTERS: Dict[str, int] = {
  "a": 1,
  "b": 4,
  "c": 4,
  "d": 2,
  "e": 1,
  "f": 4,
  "g": 3,
  "h": 3,
  "i": 1,
  "j": 10,
  "k": 5,
  "l": 2,
  "m": 4,
  "n": 2,
  "o": 1,
  "p": 4,
  "q": 10,
  "r": 1,
  "s": 1,
  "t": 1,
  "u": 2,
  "v": 5,
  "w": 4,
  "x": 8,
  "y": 3,
  "z": 10,
}
