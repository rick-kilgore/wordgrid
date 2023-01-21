
from grid import Grid
from typing import Tuple

def test_grid_by_name(name: str) -> Grid:
  match name:
    case "simple":
      grid: Grid = Grid()
      grid.at(9, 5).value = 'c'
      grid.at(10, 5).value = 'o'
      grid.at(11, 5).value = 'u'
      grid.at(12, 5).value = 'n'
      grid.at(13, 5).value = 't'
      grid.at(8, 6).value = 't'
      grid.at(9, 6).value = 'a'
      grid.at(7, 7).value = 'm'
      grid.at(8, 7).value = 'o'
      grid.at(9, 7).value = 'p'
      grid.at(8, 8).value = 'r'
      grid.at(9, 8).value = 'e'
      grid.at(10, 8).value = 'v'
      grid.at(8, 9).value = 't'
    case _:
      raise Exception(f"no test case named {name}")

  return grid

