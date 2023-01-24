#!/usr/bin/env python3

import argparse
import os
import pickle
import sys
import time
from typing import Dict, List

import test
from consts import (
  GWIDTH, GHEIGHT, MULT_SQUARES,
  SOLO_WIDTH, SOLO_HEIGHT, SOLO_SQUARES, SOLO2_SQUARES, SOLO3_SQUARES,
)
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


# main
parser = argparse.ArgumentParser(description="Sync folders with Google Drive")
parser.add_argument("-f", "--file", help="used named test data as input")
parser.add_argument("-s", "--solo", action="store_true", help="use grid for solo matches")
parser.add_argument("-2", "--solo2", action="store_true", help="use solo2 grid")
parser.add_argument("-3", "--solo3", action="store_true", help="use solo3 grid")
parser.add_argument("-t", "--test", help="used named test data as input")
parser.add_argument("-p", "--pos", nargs=2, metavar="n", help="look for words starting at x y pos")
parser.add_argument("letters", default="", help="letters from which to build words")
args = parser.parse_args()

grid: Grid
width: int = SOLO_WIDTH if args.solo or args.solo2 or args.solo3 else GWIDTH
height: int = SOLO_HEIGHT if args.solo or args.solo2 or args.solo3 else GHEIGHT
msquares: List[Dict[int, str]]
if args.solo:
  msquares = SOLO_SQUARES
elif args.solo2:
  msquares = SOLO2_SQUARES
elif args.solo3:
  msquares = SOLO3_SQUARES
else:
  msquares = MULT_SQUARES
if args.file:
  grid = grid_from_file(args.file, width, height, msquares)
elif args.test:
  grid = test.test_grid_by_name(args.test)

print(grid.show())

# letters = "thkwlfe"
trie: Trie = load_trie()
words: Dict[str, FoundWord]
if args.pos:
  x = int(args.pos[0])
  y = int(args.pos[1])
  print(f"searching from ({x},{y}) w={width} h={height} letters={args.letters}", flush=True)
  print("searching right...", flush=True)
  srch: SearchCriteria = SearchCriteria(grid, grid.at(x, y), Dir.RIGHT, args.letters, trie)
  words = findwords(srch)
  print("searching down...", flush=True)
  srch = SearchCriteria(grid, grid.at(x, y), Dir.DOWN, args.letters, trie)
  addwords(words, findwords(srch))

else:
  words = {}
  for y in range(grid.h):
    for x in range (grid.w):
      cell: Cell = grid.at(x, y)
      if cell.value is None:
        print(f"start point: ({x},{y})", flush=True)
        if x < grid.w - 1:
          srch: SearchCriteria = SearchCriteria(grid, grid.at(x, y), Dir.RIGHT, args.letters, trie)
          wlist = findwords(srch)
          addwords(words, wlist)
        if y < grid.h - 1:
          srch: SearchCriteria = SearchCriteria(grid, grid.at(x, y), Dir.DOWN, args.letters, trie)
          wlist = findwords(srch)
          addwords(words, wlist)

srtd: List[str] = sorted(words.keys(), key=lambda w: words[w].score)
out: str = "\n  ".join([str(words[w]) for w in srtd])
print(f"found:\n{out}")

print(f"\ntop 10 are:")
for w in srtd[-10:]:
  gcl: Grid = grid.clone()
  fw: FoundWord = words[w]
  print(f"  {fw}\n")
  gcl.apply(fw.word, fw.pos, fw.dirn)
  print(gcl.show(), "\n")

