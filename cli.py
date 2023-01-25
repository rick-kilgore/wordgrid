#!/usr/bin/env python3

import argparse

from grid import Grid
from main import load_board, load_trie, run_for_single_pos, run_whole_board
from search import FoundWord
from trie import Trie
from typing import Dict, List

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
  words = run_whole_board(grid, trie, args.letters)


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
