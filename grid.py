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
}

class GridDef:
  def __init__(self, w: int, h: int):
    self.w = w
    self.h = h


class CPos:
  def __init__(self, grid: GridDef, i: int):
    self.i = i
    self.x = i % grid.w
    self.y = i // grid.w


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


class Cell:
  def __init__(self, grid, pos: CPos, ctype: str):
    self.grid = grid
    self.pos: CPos = pos
    self.ctype: str = ctype
    self.value: chr = None # no letter placed at start
    self.added: bool = False

  def is_middle_cell(self) -> bool:
    return self.pos.x == self.grid.w // 2 and self.pos.y == self.grid.h // 2

  def is_anchored(self):
    up: Cell = self.grid.up_from(self)
    down: Cell = self.grid.down_from(self)
    left: Cell = self.grid.left_from(self)
    right: Cell = self.grid.right_from(self)
    return (
      (up and up.value)
      or (down and down.value)
      or (left and left.value)
      or (right and right.value)
    )


class Grid(GridDef):
  def __init__(self):
    GridDef.__init__(self, GWIDTH, GHEIGHT)
    self.size = self.w * self.h
    self.cells: List[Cell] = []
    for i in range(self.size):
      pos: CPos = CPos(self, i)
      isp = min(i, self.size - i - 1)
      ctype = specials[isp] if isp in specials else BLANK
      self.cells.append(Cell(self, pos, ctype))

  def show(self) -> str:
    showstr: str = ""
    for y in range(self.h):
      for x in range(self.w):
        cell: Cell = self.at(x, y)
        if cell.value is not None:
          esc: str = 32 if cell.added else 35
          showstr += f" [1;{esc}m{cell.value}[m "
        else:
          showstr += f" {self.at(x, y).ctype}"
      showstr += "\n"

    return showstr

  def at(self, x: int, y: int) -> Cell:
    return self.cells[self.w * y + x]

  def next_cell(self, cell: Cell, dirn: Dir) -> Cell:
    match dirn:
      case Dir.UP:
        return self.up_from(cell)
      case Dir.DOWN:
        return self.down_from(cell)
      case Dir.LEFT:
        return self.left_from(cell)
      case Dir.RIGHT:
        return self.right_from(cell)
    raise Exception(f"unrecognized direction: {dirn}")
        

  def left_from(self, cell: Cell) -> Cell:
    return self.cells[cell.pos.i - 1] if cell.pos.x > 0 else None

  def right_from(self, cell: Cell) -> Cell:
    return self.cells[cell.pos.i + 1] if cell.pos.x < self.w - 1 else None

  def up_from(self, cell: Cell) -> Cell:
    return self.cells[cell.pos.i - self.w] if cell.pos.y > 0 else None

  def down_from(self, cell: Cell) -> Cell:
    return self.cells[cell.pos.i + self.w] if cell.pos.y < self.h - 1 else None

  def upstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.UP)

  def downstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.DOWN)

  def leftstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.LEFT)

  def rightstr(self, cell: Cell) -> Tuple[str, Cell]:
    return self.string(cell, Dir.RIGHT)

  # string of letters starting from but not including
  # the passed-in cell in direction dirn, up to a blank
  # cell or the end of the board
  def string(self, cell: Cell, dirn: Dir) -> Tuple[str, Cell]:
    string: str = ""
    end: Cell = None
    nxt: Cell = self.next_cell(cell, dirn)
    while (nxt is not None and nxt.value is not None):
      string += nxt.value
      end = nxt
      nxt = self.next_cell(nxt, dirn)

    return string, end



def grid_copy(oldgrid: Grid) -> Grid:
  # fixme: need to not initialize the cells array every time
  newgrid = Grid()
  for i, c in enumerate(oldgrid.cells):
    newcell = Cell(newgrid, c.pos, c.ctype)
    newcell.value = c.value
    newcell.added = c.added
    newgrid.cells[i] = newcell
  return newgrid


def grid_add_letter(grid: Grid, pos: CPos, letter: chr) -> None:
  grid.cells[pos.i].value = letter
  grid.cells[pos.i].added = True

