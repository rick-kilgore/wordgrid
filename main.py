#!/usr/bin/python3

import os
import pickle
import time
from trie import Trie, TrieNode

from grid import Grid

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
      if len(w) > 0:
        dictwords.insert(word)

    report_time(f"writing dictionary to {pickle_filename}")
    with open(pickle_filename, "wb") as picklefile:
      pickle.dump(dictwords, picklefile)

  return dictwords


# main
grid: Grid = Grid()
for y in range(grid.h):
  for x in range(grid.w):
    print(f" {grid.at(x, y).ctype}", end="")
  print()
