import json
from typing import Dict

from grid import Grid
from search import (
  FoundWord, search_from_row, search_from_single_pos, search_whole_board
)
from trie import Trie
from utils import display_results, load_board, load_trie

trie = None


def handle_findwords(event, ctx) -> str:
  print(f"request: {event}")
  grid: Grid
  if "board" in event:
    grid = Grid.deserialize(event["board"])
  verbose: bool = "verbose" in event and event["verbose"] > 0
  global trie
  if trie is None:
    trie = load_trie(False)
  words: Dict[str, FoundWord]
  if "x" in event and "y" in event:
    words = search_from_single_pos(grid, trie, event["letters"], int(event["x"]), int(event["y"]), verbose)
  elif "row" in event:
    words = search_from_row(grid, trie, event["letters"], int(event["row"]), verbose)
  else:
    words = search_whole_board(grid, trie, event["letters"], verbose)

  num_details = int(event["details"]) if "details" in event else 5
  bylen = True if "bylen" in event and event["bylen"] else False
  rsp: str = display_results(grid, words, num_details, bylen)
  return rsp.encode('utf-8')
