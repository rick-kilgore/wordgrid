import functions_framework
from flask import Request

import json
from typing import Dict

from grid import Grid
from search import FoundWord, search_from_single_pos, search_whole_board
from trie import Trie
from utils import display_results, load_board, load_trie

@functions_framework.http
def http(req: Request) -> str:
  data = json.loads(req.data)
  print(f"request: {data}")
  grid: Grid = load_board(data["board"], data["file"])
  trie: Trie = load_trie()
  words: Dict[str, FoundWord]
  if "x" in data and "y" in data:
    words = str(search_from_single_pos(grid, trie, data["letters"], data["x"], data["y"]))
  else:
    words = search_whole_board(grid, trie, data["letters"])

  num_details = int(data["details"]) if "details" in data else 5
  rsp: str = display_results(grid, words, num_details)
  return rsp
