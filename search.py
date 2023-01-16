#!/usr/bin/python3

from typing import Dict
from trie import Trie

from grid import (
  Cell, Dir, Grid, grid_add_letter, grid_copy, opposite,
)

class SearchCriteria:
  def __init__(self, grid: Grid, start: Cell, dirn: Dir, letters: str):
    self.grid = grid
    self.start = start
    self.dirn = dirn
    self.letters = letters

class SearchContext:
  def __init__(self, srch: SearchCriteria):
    self.srch: SearchCriteria = srch
    self.grid: Grid = srch.grid
    self.dirn: Dir = srch.dirn
    self.cell: Cell = srch.start
    self.letters: str = srch.letters
    self.sofar: str = ""
    self.is_anchored = srch.start.is_middle_cell()

def add_letter(ctx: SearchContext, ch: chr, depth: int) -> SearchContext:
  sofar: str = ctx.sofar + ch
  letters = ctx.letters.replace(ch, '', 1)
  nxt_ctx = ctx_advance(ctx, sofar, letters)
  grid_add_letter(nxt_ctx.grid, ctx.cell.pos, ch)
  return nxt_ctx

def add_existing(ctx: SearchContext) -> SearchContext:
  sofar: str = ctx.sofar + ctx.cell.value
  return ctx_advance(ctx, sofar, ctx.letters)

def ctx_advance(ctx: SearchContext, sofar: str, letters: str) -> SearchContext:
  nxt: Cell = ctx.grid.next_cell(ctx.cell, ctx.dirn)
  nxt_ctx = SearchContext(ctx.srch)
  nxt_ctx.grid = grid_copy(ctx.grid)
  nxt_ctx.cell = nxt
  nxt_ctx.sofar = sofar
  nxt_ctx.letters = letters
  nxt_ctx.is_anchored = ctx.is_anchored or ctx.cell.is_anchored()
  return nxt_ctx

def is_word_boundary(cell: Cell) -> bool:
  return cell is None or cell.value is None

def findwords(srch: SearchCriteria, trie: Trie) -> Dict[str, int]:
  if srch.start.value is not None:
    print("can't start a search from a cell that already has a value: "
          f"({srch.start.pos.x},{srch.start.pos.y})={srch.start.value}")
    return {}

  ctx: SearchContext = SearchContext(srch)
  ctx.sofar, _ = srch.grid.string(srch.start, opposite(srch.dirn))
  return search(ctx, trie, 0)


def unique_letters(letters: str) -> str:
  out: str = ""
  for ch in letters:
    if ch not in out:
      out += ch
  return out


def search(ctx: SearchContext, trie: Trie, depth: int) -> Dict[str, int]:
  words: Dict[str, int] = {}
  cell: Cell = ctx.cell
  if cell is not None:
    if cell.value is None:
      letters = ctx.letters
      for ch in unique_letters(letters):
        was: str = ctx.sofar
        nxt_ctx = add_letter(ctx, ch, depth)
        # print(f"{'  ' * depth}{was} -> {nxt_ctx.sofar}       ({nxt_ctx.letters})")

        # fixme: probably should keep TrieNode so this check is O(1)
        tnode: TrieNode = trie.isprefix(nxt_ctx.sofar)
        if tnode is not None:
          if is_word_boundary(nxt_ctx.cell) and tnode.isword and nxt_ctx.is_anchored:
            addword(nxt_ctx, words)
          addwords(words, search(nxt_ctx, trie, depth+1))

    else:
      nxt_ctx = add_existing(ctx)
      tnode: TrieNode = trie.isprefix(nxt_ctx.sofar)
      if tnode is not None:
        if is_word_boundary(nxt_ctx.cell) and tnode.isword:
          addword(nxt_ctx, words)
        addwords(words, search(nxt_ctx, trie, depth+1))

  return words

def addword(ctx: SearchContext, words: Dict[str, int]) -> None:
  words[ctx.sofar] = len(ctx.sofar)
  print(f"'{ctx.sofar}' at ({ctx.cell.pos.x},{ctx.cell.pos.y})", flush=True)
  print(ctx.grid.show() + "\n", flush=True)
  

def addwords(dest: Dict[str, int], src: Dict[str, int]) -> None:
  for k in src:
    if k not in dest or src[k] > dest[k]:
      dest[k] = src[k]
