
import os
import pickle
from typing import Dict, List, Tuple

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
  return grid


def load_trie(words_file: str, use_pickle: bool = True) -> Trie:
  dictwords = Trie()
  pickle_filename = f"{words_file}.pickle"
  if use_pickle and os.path.exists(pickle_filename):
    with open(pickle_filename, "rb") as picklefile:
      print(f"loading words from {pickle_filename}")
      return pickle.load(picklefile)

  with open(words_file) as dictfile:
    print(f"loading words from {words_file}")
    lines = dictfile.readlines()

    for line in lines:
      word = line.lower().strip()
      if len(word) > 0:
        dictwords.insert(word)

    if use_pickle:
      with open(pickle_filename, "wb") as picklefile:
        pickle.dump(dictwords, picklefile)

  return dictwords


def display_results(grid: Grid, words: Dict[str, FoundWord], details_count: int, sortbylen: bool = False) -> str:
  def keyfunc(w: str) -> Tuple[int, int]:
    return (len(w), words[w].score) if sortbylen else (words[w].score, len(w))

  srtd: List[str] = sorted(words.keys(), key=keyfunc)
  disp_str = "found:\n  " + "\n  ".join([str(words[w]) for w in srtd]) + "\n"

  if details_count > 0:
    disp_str += f"\n\ntop {details_count} are:\n\n"
    for i, w in enumerate(srtd[-details_count:]):
      gcl: Grid = grid.clone()
      fw: FoundWord = words[w]
      disp_str += f"{details_count - i:02}: {fw}\n"
      gcl.apply(fw.word, fw.pos, fw.dirn)
      disp_str += gcl.show() + "\n"

  return disp_str
