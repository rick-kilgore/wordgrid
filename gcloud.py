import functions_framework
from flask import Request

import json
from typing import Dict

from grid import Grid
from search import FoundWord
from trie import Trie
from utils import load_board, load_trie

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
