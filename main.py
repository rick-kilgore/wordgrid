#!/usr/bin/env python3

import argparse
import os
import pickle
import sys
import time
from typing import Dict, List

import test
from consts import get_board_data
from grid import Cell, Dir, Grid, grid_from_file
from search import (
  SearchCriteria, FoundWord, findwords, addwords,
)
from trie import Trie, TrieNode


last_time = -1.0
def report_time(msg: str) -> None:
  now = time.process_time()
  global last_time
  if last_time >= 0.0:
    print(f"{msg}: elapsed = {now - last_time}")
  else:
    print(f"{msg}: time = {now}")
  last_time = now

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

    report_time(f"writing dictionary to {pickle_filename}")
    with open(pickle_filename, "wb") as picklefile:
      pickle.dump(dictwords, picklefile)

  return dictwords
  

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

def run_for_single_pos(grid: Grid, trie: Trie, letters: str, startx: int, starty: int) -> Dict[str, FoundWord]:
  print(f"searching from ({startx},{starty})", flush=True)
  words: Dict[str, FoundWord] = {}
  if startx < grid.w - 1:
    # print("searching right...", flush=True)
    srch = SearchCriteria(grid, grid.at(startx, starty), Dir.RIGHT, letters, trie)
    words = findwords(srch)
  if starty < grid.h - 1:
    # print("searching down...", flush=True)
    srch = SearchCriteria(grid, grid.at(startx, starty), Dir.DOWN, letters, trie)
    addwords(words, findwords(srch))
  return words


def run_whole_board(grid: Grid, trie: Trie, file: str, letters: str) -> Dict[str, FoundWord]:
  words: Dict[str, FoundWord] = {}
  for y in range(grid.h):
    for x in range (grid.w):
      cell: Cell = grid.at(x, y)
      if cell.value is None:
        addwords(words, run_for_single_pos(grid, trie, letters, x, y))

  return words


# main
parser = argparse.ArgumentParser(description="Sync folders with Google Drive")
parser.add_argument("-f", "--file", help="used named test data as input")
parser.add_argument("-b", "--board", default=0, type=int, metavar="VERSION", help="use one of the solo match grids")
parser.add_argument("-t", "--test", help="used named test data as input")
parser.add_argument("-p", "--pos", nargs=2, type=int, metavar="N", help="look for words starting at x y pos")
parser.add_argument("letters", default="", help="letters from which to build words")
args = parser.parse_args()

grid: Grid = load_board(args.board, args.file)
trie: Trie = load_trie()
words: Dict[str, FoundWord]
if args.pos:
  words = run_for_single_pos(grid, trie, args.letters, args.pos[0], args.pos[1])
else:
  words = run_whole_board(grid, trie, args.file, args.letters)


srtd: List[str] = sorted(words.keys(), key=lambda w: words[w].score)
full: str = "\n  ".join([str(words[w]) for w in srtd])
print(f"found:\n{full}")

print(f"\ntop 10 are:")
for w in srtd[-10:]:
  gcl: Grid = grid.clone()
  fw: FoundWord = words[w]
  print(f"  {fw}\n")
  gcl.apply(fw.word, fw.pos, fw.dirn)
  print(gcl.show(), "\n")

