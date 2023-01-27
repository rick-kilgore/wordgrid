
from enum import Enum
from typing import Dict, List, Tuple


BLANK: str = "__"
DL: str = "DL"
TL: str = "TL"
DW: str = "DW"
TW: str = "TW"

GWIDTH: int = 15
GHEIGHT: int = 15
SOLO_WIDTH: int = 11
SOLO_HEIGHT: int = 11

boards: List[List[Dict[int, str]]] = [
  # board used against other players
  [
    { 3: TW, 6: TL, 8: TL, 11: TW, },
    { 2: DL, 5: DW, 9: DW, 12: DL, },
    { 1: DL, 4: DL, 10: DL, 13: DL, },
    { 0: TW, 3: TL, 7: DW, 11: TL, 14: TW, },
    { 2: DL, 6: DL, 8: DL, 12: DL, },
    { 1: DW, 5: TL, 9: TL, 13: DW, },
    { 0: TL, 4: DL, 10: DL, 14: TL, },
    { 3: DW, 11: DW, },
  ],

  # 1st solo challenge board
  [
    { 0: TL, 2: TW, 8: TW, 10: TL, },
    { 1: DW, 5: DW, 9: DW, },
    { 0: TW, 2: DL, 4: DL, 6: DL, 8: DL, 10: TW, },
    { 3: TL, 7: TL, },
    { 2: DL, 8: DL, },
    { 1: DW, 63: DW, },
  ],

  # 2nd solo challenge board
  [
    { 0: TW, 3: DL, 4: TL, 7: DL, 8: TW, },
    { 0: DL, 1: DW, 4: DL, 5: DL, 8: DL, 9: DW, },
    { 1: DL, 2: TW, 5: DL, 6: TL, 9: DL, 10: TW, },
    { 2: DL, 3: DW, 6: DL, 7: DW, 10: DL, },
    { 0: DL, 3: DL, 4: DL, 7: DL, 8: DL, },
    { 0: TL, 1: DL, 4: DL, },
  ],

  # 3rd solo challenge board
  [
    { 0: TW, 4: DL, 5: DL, 6: DL, 10: TW, },
    { 1: DW, 3: DL, 4: DL, 5: DL, 6: DL, 7: DL, 9: DW, },
    { 2: DL, 3: DL, 7: DL, 8: DL, },
    { 0: TL, 2: DL, 8: DL, 10: TL, },
    { 1: TL, 2: DL, 4: DL, 6: DL, 8: DL, 9: TL, },
    { 2: DL, 8: DL, },
    { 1: TL, 3: DL, 7: DL, 9: TL, },
    { 0: TL, 4: DL, 5: DL, 6: DL, 10: TL, },
    { 2: DW, 4: DL, 6: DL, 9: DW, },
    { 1: TL, 4: DL, 6: DL, 9: TL, },
    { 0: TW, 5: TL, 10: TW, },
  ],

  # 4th solo challenge board
  [
    { 0: TW, 1: DL, 2: DL, 5: TL, 8: DL, 9: DL, 10: TW, },
    { 0: DL, 1: DL, 4: DL, 5: DL, 6: DL, 9: DL, 10: DL, },
    { 0: DL, 2: DW, 4: DL, 6: DL, 8: DW, 10: DL, },
    { },
    { 1: DL, 2: DL, 4: DL, 6: DL, 8: DL, 9: DL, },
    { 0: TL, 1: DL, 9: DL, 10: TL, },
  ],

  # 5th solo challenge board
  [
    { 5: DW, },
    { 1: TW, 4: DL, 6: DL, 9: TW, },
    { 2: TL, 3: DL, 4: DL, 6: DL, 7: DL, 8: TL, },
    { 2: DL, 5: DL, 8: DL, },
    { 1: DL, 2: DL, 4: DL, 6: DL, 8: DL, 9: DL, },
    { 0: DW, 3: DL, 7: DL, 10: DW, },
  ],

  # 6th solo challenge board
  [
    { 0: TW, 5: TW, 10: TW },
    { 1: DW, 3: TL, 5: DL, 7: TL, 9: DW },
    { 2: TL, 4: DL, 6: DL, 8: TL },
    { 1: TL, 3: DW, 5: DL, 7: DW, 9: TL },
    { 2: DL, 4: DL, 6: DL, 8: DL },
    { 0: TW, 1: DL, 3: DL, 7: DL, 9: DL, 10: TW },
  ],
]

# returns [grid_width, grid_height, grid_spec]
def get_board_data(board_num: int) -> Tuple[int, int, List[Dict[int, str]]]:
  width: int = GWIDTH if board_num == 0 else SOLO_WIDTH
  height: int = GHEIGHT if board_num == 0 else SOLO_HEIGHT
  return width, height, boards[board_num]

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
