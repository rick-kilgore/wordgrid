#!/usr/bin/env python3

import argparse
from typing import Dict, List

from grid import Grid
from search import FoundWord, search_from_single_pos, search_whole_board
from trie import Trie
from utils import display_results, load_board, load_trie

parser = argparse.ArgumentParser(description="load/print and (de)serialize a grid")
parser.add_argument("-f", "--file", help="input file holding the state of the board")
parser.add_argument("-b", "--board", default=0, type=int, metavar="VERSION", help="board size: 0=pvp, 1, 2, ... solo boards")
parser.add_argument("string", default="", nargs="?", help="serialized board as a string")
args = parser.parse_args()

if args.file:
  grid: Grid = load_board(args.board, args.file)
  print(f"{grid.serialize()}")
elif args.string:
  grid: Grid = Grid.deserialize(args.string)
  print(grid.show())

