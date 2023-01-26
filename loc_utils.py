
import parse
from consts import Dir
from grid import GridDef, CPos
from search import FoundWord

def foundWordFromStr(grid: GridDef, string: str) -> FoundWord:
  score, word, dirn, x, y = parse.parse("{}: {} {} from ({},{})", string)
  pos = CPos(grid, grid.w * int(y) + int(x))
  return FoundWord(word, int(score), pos, Dir[dirn])
