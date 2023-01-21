from typing import Any, Dict, List, Optional, Tuple

import consts
from consts import (
  BLANK, GWIDTH, GHEIGHT,
  Dir, opposite, MULT_SQUARES,
)

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


  # WARNING: this method assumes the caller knows
  # what they are doing in that the requested
  # traversal will not go off the board
  def traverse(self, ncells: int, dirn: Dir): # -> CPos
    match dirn:
      case Dir.UP:
        return CPos(self.grid, self.i - (self.grid.w * ncells))
      case Dir.DOWN:
        return CPos(self.grid, self.i + (self.grid.w * ncells))
      case Dir.LEFT:
        return CPos(self.grid, self.i - ncells)
      case Dir.RIGHT:
        return CPos(self.grid, self.i + ncells)
      case _:
        raise Exception(f"unrecognized direction: {dirn}")

class Cell:
  def __init__(self, grid, pos: CPos, ctype: str, value: Optional[str] = None):
    self.grid = grid
    self.pos: CPos = pos
    self.ctype: str = ctype
    self.value: Optional[str] = value
    self.added: bool = False

  def letter_mult(self) -> int:
    match self.ctype:
      case consts.DL:
        return 2
      case consts.TL:
        return 3
      case _:
        return 1

  def word_mult(self) -> int:
    match self.ctype:
      case consts.DW:
        return 2
      case consts.TW:
        return 3
      case _:
        return 1

  def is_middle_cell(self) -> bool:
    return self.pos.x == self.grid.w // 2 and self.pos.y == self.grid.h // 2

  def is_anchored(self):
    up: Optional[Cell] = self.grid.up_from(self)
    down: Optional[Cell] = self.grid.down_from(self)
    left: Optional[Cell] = self.grid.left_from(self)
    right: Optional[Cell] = self.grid.right_from(self)
    return (
      (up is not None and up.value is not None and not up.added)
      or (down is not None and down.value is not None and not down.added)
      or (left is not None and left.value is not None and not left.added)
      or (right is not None and right.value is not None and not right.added)
    )


class Grid(GridDef):
  def __init__(self, init=True):
    GridDef.__init__(self, GWIDTH, GHEIGHT)
    if init:
      self.size = self.w * self.h
      self.cells: List[Cell] = []
      for i in range(self.size):
        pos: CPos = CPos(self, i)
        isp = min(i, self.size - i - 1)
        ctype = MULT_SQUARES[isp] if isp in MULT_SQUARES else BLANK
        self.cells.append(Cell(self, pos, ctype))


  def clone(self) -> Any:
    newgrid: Grid = Grid(False)
    newgrid.w = self.w
    newgrid.h = self.h
    newgrid.size = self.size
    newgrid.cells = []
    for cell in self.cells:
      newgrid.cells.append(Cell(newgrid, cell.pos, cell.ctype, cell.value))
    return newgrid


  def show(self) -> str:
    showstr: str = "   "
    for i in range(self.w):
      showstr += f" {i}".rjust(3, ' ')
    showstr += "\n"
    for y in range(self.h):
      showstr += f" {y}".rjust(3, ' ')
      for x in range(self.w):
        cell: Cell = self.at(x, y)
        if cell.value is not None:
          esc: int = 32 if cell.added else 35
          showstr += f" [1;{esc}m{cell.value}[m "
        else:
          showstr += f" {self.at(x, y).ctype}"
      showstr += "\n"

    return showstr

  def apply(self, word: str, startpos: CPos, dirn: Dir) -> None:
    pos: CPos = startpos
    for i in range(len(word)):
      cell: Cell = self.cells[pos.i] 
      if cell.value is None:
        cell.value = word[i]
        cell.added = True
      elif cell.value != word[i]:
        raise Exception(
          f"failure applying word {word}: found existing letter {cell.value} "
          f"at ({pos.x},{pos.y}) instead of {word[i]}"
        )
      pos = pos.traverse(1, dirn)

  def at(self, x: int, y: int) -> Cell:
    return self.cells[self.w * y + x]

  def next_cell(self, cell: Cell, dirn: Dir) -> Optional[Cell]:
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
        

  def left_from(self, cell: Cell) -> Optional[Cell]:
    return self.cells[cell.pos.i - 1] if cell.pos.x > 0 else None

  def right_from(self, cell: Cell) -> Optional[Cell]:
    return self.cells[cell.pos.i + 1] if cell.pos.x < self.w - 1 else None

  def up_from(self, cell: Cell) -> Optional[Cell]:
    return self.cells[cell.pos.i - self.w] if cell.pos.y > 0 else None

  def down_from(self, cell: Cell) -> Optional[Cell]:
    return self.cells[cell.pos.i + self.w] if cell.pos.y < self.h - 1 else None

  def upstr(self, cell: Cell) -> Tuple[str, Optional[Cell]]:
    strpath, start = self.string(cell, Dir.UP)
    return strpath[::-1], start

  def downstr(self, cell: Cell) -> Tuple[str, Optional[Cell]]:
    return self.string(cell, Dir.DOWN)

  def leftstr(self, cell: Cell) -> Tuple[str, Optional[Cell]]:
    strpath, start = self.string(cell, Dir.LEFT)
    return strpath[::-1], start

  def rightstr(self, cell: Cell) -> Tuple[str, Optional[Cell]]:
    return self.string(cell, Dir.RIGHT)

  # string of letters starting from but not including
  # the passed-in cell in direction dirn, up to a blank
  # cell or the end of the board
  def string(self, cell: Cell, dirn: Dir) -> Tuple[str, Optional[Cell]]:
    string: str = ""
    end: Optional[Cell] = None
    nxt: Optional[Cell] = self.next_cell(cell, dirn)
    while (nxt is not None and nxt.value is not None):
      string += nxt.value
      end = nxt
      nxt = self.next_cell(nxt, dirn)

    return string, end


def grid_from_file(fname: str) -> Grid:
  grid: Grid = Grid()
  with open(fname, "r") as file:
    line: int = 0
    while line < grid.h:
      row: List[str] = file.readline().strip().split()
      for i, s in enumerate(row):
        if s != "-":
          grid.at(i, line).value = s
      line += 1
  return grid


def grid_copy(oldgrid: Grid) -> Grid:
  # fixme: need to not initialize the cells array every time
  newgrid = Grid()
  for i, c in enumerate(oldgrid.cells):
    newcell = Cell(newgrid, c.pos, c.ctype)
    newcell.value = c.value
    newcell.added = c.added
    newgrid.cells[i] = newcell
  return newgrid


def grid_add_letter(grid: Grid, pos: CPos, letter: str) -> None:
  grid.cells[pos.i].value = letter
  grid.cells[pos.i].added = True

