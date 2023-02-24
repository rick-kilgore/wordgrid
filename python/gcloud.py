import functions_framework
from flask import Request

import json
from typing import Dict

from grid import Grid
from search import (
  FoundWord, search_from_row, search_from_single_pos, search_whole_board
)
from trie import Trie
from utils import display_results, load_board, load_trie

trie = None


@functions_framework.http
def http(req: Request) -> str:
  data = json.loads(req.data)
  print(f"request: {data}")
  grid: Grid
  if "board" in data:
    grid = Grid.deserialize(data["board"])
  global trie
  if trie is None:
    trie = load_trie()
  words: Dict[str, FoundWord]
  if "x" in data and "y" in data:
    words = search_from_single_pos(grid, trie, data["letters"], int(data["x"]), int(data["y"]))
  elif "row" in data:
    words = search_from_row(grid, trie, data["letters"], int(data["row"]))
  else:
    words = search_whole_board(grid, trie, data["letters"])

  num_details = int(data["details"]) if "details" in data else 5
  bylen = True if "bylen" in data and data["bylen"] else False
  rsp: str = display_results(grid, words, num_details, bylen)
  return rsp
