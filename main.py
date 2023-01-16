#!/usr/bin/python3

import os
import pickle
import sys
import time

from trie import Trie, TrieNode
from grid import Cell, Dir, Grid
from search import (
  SearchCriteria, findwords,
)

last_time = -1.0
def report_time(msg: str) -> float:
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
grid: Grid = Grid()
grid.at(7, 7).value = 'a'
print(grid.show())

trie: Trie = load_trie()
x, y = int(sys.argv[1]), int(sys.argv[2])
srch: SearchCriteria = SearchCriteria(grid, grid.at(x, y), Dir.DOWN, "plpe")
words = findwords(srch, trie)
print(words)

