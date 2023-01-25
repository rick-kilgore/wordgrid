#!/usr/bin/env python3

import functions_framework
from flask import Request

import json
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
from trie import Trie


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


def run_whole_board(grid: Grid, trie: Trie, letters: str) -> Dict[str, FoundWord]:
  words: Dict[str, FoundWord] = {}
  for y in range(grid.h):
    for x in range (grid.w):
      cell: Cell = grid.at(x, y)
      if cell.value is None:
        addwords(words, run_for_single_pos(grid, trie, letters, x, y))

  return words


@functions_framework.http
def http(req: Request) -> str:
  print(f"req.data: {type(req.data)}: {req.data}")
  data = json.loads(req.data)
  print(f"data: {type(data)}: {data}")
  grid: Grid = load_board(data["board"], data["file"])
  trie: Trie = load_trie()
  # return str(run_for_single_pos(grid, trie, data["letters"], data["x"], data["y"]))
  words: Dict[str, FoundWord] = run_whole_board(grid, trie, data["letters"])
  srtd: List[str] = sorted(words.keys(), key=lambda w: words[w].score)
  rsp: str = ""
  for w in srtd:
    rsp += str(words[w]) + "\n"
  for w in srtd[-5:]:
    rsp += w + "\n"
    rsp += grid.clone().apply(w, words[w].pos, words[w].dirn).show() + "\n"
  return rsp

