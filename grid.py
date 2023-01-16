#!/usr/bin/python3

from enum import Enum
from typing import Dict, List, Tuple


BLANK: str = "__"
DL: str = "DL"
TL: str = "TL"
DW: str = "DW"
TW: str = "TW"

GWIDTH: int = 15
GHEIGHT: int = 15
specials: Dict[int, str] = {
  3: TW, 6: TL, 8: TL, 11: TW,
  17: DL, 20: DW, 24: DW, 27: DL,
  31: DL, 34: DL, 40: DL, 43: DL,
  45: TW, 48: TL, 52: DW, 56: TL, 59: TW,
  62: DL, 66: DL, 68: DL, 72: DL,
  76: DW, 80: TL, 84: TL, 88: DW,
  90: TL, 94: DL, 100: DL, 104: TL,
  108: DW, 116: DW,
#  120: TL, 124: DL, 130: DL, 134: TL,
#  136: DW, 140: TL, 144: TL, 148: DW,
#  152: DL, 156: DL, 158: DL, 162: DL,
#  165: TW, 168: TL, 172: DW, 176: TL, 179: TW,
#  181: DL, 184: DL, 190: DL, 193: DL,
#  197: DL, 200: DW, 204: DW, 207: DL,
#  213: TW, 216: TL, 218: TL, 221: TW,
}

class GridDef:
  def __init__(self, w: int, h: int):
    self.w = w
    self.h = h


class CPos:
  def __init__(self, grid: GridDef, i: int):
    self.grid = grid
    self.i = i
    self.x = i % grid.w
    self.y = i // grid.w


class Dir(Enum):
  UP = 1
  RIGHT = 2
  DOWN = 3
  LEFT = 4


class Cell:
  def __init__(self, pos: CPos, ctype: str):
    self.grid = pos.grid
    self.pos = pos
    self.ctype = ctype
    self.value = None # no letter placed at start
    


class Grid(GridDef):
  def __init__(self):
    GridDef.__init__(self, GWIDTH, GHEIGHT)
    self.size = self.w * self.h
    self.cells: List[Cell] = []
    for i in range(self.size):
      pos: CPos = CPos(self, i)
      isp = min(i, self.size - i - 1)
      ctype = specials[isp] if isp in specials else BLANK
      self.cells.append(Cell(pos, ctype))

  def at(self, x: int, y: int) -> Cell:
    return self.cells[self.w * y + x]

  def set(self, x: int, y: int, cell: Cell) -> None:
    self.cells[self.w * y + x] = cell

  def next_cell(self, cell: Cell, dir: Dir) -> Cell:
    match dir:
      case Dir.UP:
        return self.up()
      case Dir.DOWN:
        return self.down()
      case Dir.LEFT:
        return self.left()
      case Dir.RIGHT:
        return self.right()
    raise f"unrecognized direction: {dir}"
        

  def left(self, cell: Cell) -> Cell:
    return self.grid[self.pos.i - 1] if self.pos.x > 0 else None

  def right(self, cell: Cell) -> Cell:
    return self.grid[self.pos.i + 1] if self.pos.x < self.grid.w - 1 else None

  def up(self, cell: Cell) -> Cell:
    return self.grid[self.pos.i - self.grid.w] if self.pos.y > 0 else None

  def down(self, cell: Cell) -> Cell:
    return self.grid[self.pos.i + self.grid.w] if self.pos.y < self.grid.h - 1 else None

  def upstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.UP)

  def downstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.DOWN)

  def leftstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.LEFT)

  def rightstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.RIGHT)

  def string(self, cell: Cell, dir: Dir) -> Tuple[str, Cell]:
    string: str = ""
    end: Cell = None
    nxt: Cell = self.next_cell(dir)
    while (nxt is not None and nxt.value is not None):
      string += nxt.value
      end = nxt
      nxt = nxt.next_cell(dir)

    return string, end
