
import os
import pickle
from typing import Dict, List

from consts import get_board_data
from grid import Grid, grid_from_file
from search import FoundWord
from trie import Trie


def load_board(board_num: int, file: str) -> Grid:
  grid: Grid
  width: int
  height: int
  bspec: List[Dict[int, str]]
  width, height, bspec = get_board_data(board_num)

  grid = grid_from_file(file, width, height, bspec)
  # grid = test.test_grid_by_name(test_name)
  print(grid.show())
  return grid


def load_trie() -> Trie:
  dictwords = Trie()
  pickle_filename = "words.pickle" 
  if os.path.exists(pickle_filename):
    with open(pickle_filename, "rb") as picklefile:
      return pickle.load(picklefile)

  with open(f"wwf.txt") as dictfile:
    lines = dictfile.readlines()

    for line in lines:
      word = line.lower().strip()
      if len(word) > 0:
        dictwords.insert(word)

    print(f"writing dictionary to {pickle_filename}")
    with open(pickle_filename, "wb") as picklefile:
      pickle.dump(dictwords, picklefile)

  return dictwords

def display_results(grid: Grid, words: Dict[str, FoundWord], details_count: int = 10) -> None:
  srtd: List[str] = sorted(words.keys(), key=lambda w: words[w].score)
  full: str = "\n  ".join([str(words[w]) for w in srtd])
  print(f"found:\n{full}")

  print(f"\ntop {details_count} are:")
  for i, w in enumerate(srtd[-details_count:]):
    gcl: Grid = grid.clone()
    fw: FoundWord = words[w]
    print(f"{details_count - i:02}: {fw}\n")
    gcl.apply(fw.word, fw.pos, fw.dirn)
    print(gcl.show(), "\n")
