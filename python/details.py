#!/usr/bin/env python3

import argparse
import re
import sys
from typing import Dict, List

from grid import Grid
from loc_utils import foundWordFromStr
from search import FoundWord
from utils import display_results

parser = argparse.ArgumentParser(description="convert text results (read from stdin) into visual ones")
parser.add_argument("boardstr", default="", help="serialized board as a string")
parser.add_argument("-n", "--num", type=int, default=10, metavar="NUM", help="number of detailed results to show")
args = parser.parse_args()

grid: Grid = Grid.deserialize(args.boardstr)
words: Dict[str, FoundWord] = {}
for line in sys.stdin:
  line = line.strip()
  if re.match(r"\s*\d+:\s+\w+\s+(right|down)", line, re.IGNORECASE):
    fw = foundWordFromStr(grid, line)
    words[fw.word] = fw

print(display_results(grid, words, args.num))
