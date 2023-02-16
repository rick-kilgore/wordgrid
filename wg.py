#!/usr/bin/env python3

import argparse
from typing import Dict, List

from grid import Grid
from search import FoundWord, search_from_row, search_from_single_pos, search_whole_board
from trie import Trie
from utils import display_results, load_board, load_trie

parser = argparse.ArgumentParser(description="Find words on a scrabble board")
parser.add_argument("-f", "--file", help="board represted by file as input")
parser.add_argument("-b", "--board", default=0, type=int, metavar="VERSION", help="use one of the solo match grids")
parser.add_argument("-p", "--pos", nargs=2, type=int, metavar="N", help="look for words starting at x y pos")
parser.add_argument("-r", "--row", type=int, metavar="N", help="look for words starting in row N")
parser.add_argument("-d", "--details", type=int, default=5, metavar="NUM", help="number of details results to show")
parser.add_argument("-l", "--len", action="store_true", help="sort by word length")
parser.add_argument("-v", "--verbose", action="store_true", help="print some debugging info on console")
parser.add_argument("-w", "--wordsfile", help="use a different words file")
parser.add_argument("letters", default="", help="letters from which to build words")
args = parser.parse_args()

def log(msg: str):
  if args.verbose:
    print(msg, flush=True)

grid: Grid = load_board(args.board, args.file)
log(grid.show())
trie: Trie = load_trie(args.wordsfile if args.wordsfile else "wwf.txt", False)
words: Dict[str, FoundWord]
if args.pos:
  words = search_from_single_pos(grid, trie, args.letters, args.pos[0], args.pos[1], args.verbose)
elif args.row:
  words = search_from_row(grid, trie, args.letters, args.row, args.verbose)
else:
  words = search_whole_board(grid, trie, args.letters, args.verbose)

print(display_results(grid, words, args.details, args.len))

