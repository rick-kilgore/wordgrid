#!/usr/bin/python3

from typing import Dict, Optional, Tuple

from consts import LETTERS
from grid import (
  Cell, CPos, Dir, Grid, grid_copy, opposite,
)
from trie import Trie, TrieNode

class SearchCriteria:
  def __init__(self, grid: Grid, start: Cell, dirn: Dir, letters: str, trie: Trie):
    self.grid = grid
    self.start_cell = start
    self.dirn = dirn
    self.letters = letters
    self.trie = trie

class SearchContext:
  def __init__(self, srch: SearchCriteria, first_move: bool = False):
    self.srch: SearchCriteria = srch
    self.grid: Grid = srch.grid
    self.cell: Optional[Cell] = srch.start_cell
    self.letters: str = srch.letters
    self.sofar: str = ""
    self.score: int = 0
    self.scoreadd: int = 0
    self.scoremult: int = 1
    self.is_anchored = first_move

def clone_context(ctx: SearchContext) -> SearchContext:
  nxt: SearchContext = SearchContext(ctx.srch)
  nxt.grid = ctx.grid
  nxt.cell = ctx.cell
  nxt.letters = ctx.letters
  nxt.sofar = ctx.sofar
  nxt.score = ctx.score
  nxt.scoreadd = ctx.scoreadd
  nxt.scoremult = ctx.scoremult
  nxt.is_anchored = ctx.is_anchored
  return nxt

class FoundWord:
  def __init__(self, word: str, score: int, pos: CPos, dirn: Dir):
    self.word = word
    self.score = score
    self.pos = pos
    self.dirn = dirn

  def __str__(self) -> str:
    return f"{self.word} at ({self.pos.x},{self.pos.y}) dirn={self.dirn} score={self.score}"

  def __repr__(self) -> str:
    return str(self)

# ctx contains the Cell to which we are adding the letter
# the returned nxt_ctx points to the next Cell in the search direction
def add_letter(ctx: SearchContext, cell: Cell, ch: str, depth: int) -> Tuple[SearchContext, Optional[Cell]]:
  sofar: str = ctx.sofar + ch
  letters = ctx.letters.replace(ch, '', 1)
  nxt_cell = ctx.grid.next_cell(cell, ctx.srch.dirn)
  nxt_ctx: SearchContext = next_context(ctx, nxt_cell, sofar, letters)
  nxt_ctx.score += LETTERS[ch.lower()] * cell.letter_mult()
  nxt_ctx.scoremult *= cell.word_mult()
  return nxt_ctx, nxt_cell

# ctx contains the Cell with the letter we are adding to sofar
# the returned nxt_ctx points to the next Cell in the search direction
def add_existing(ctx: SearchContext, cell: Cell) -> Tuple[SearchContext, Optional[Cell]]:
  assert cell.value is not None
  sofar: str = ctx.sofar + cell.value
  nxt_cell = ctx.grid.next_cell(cell, ctx.srch.dirn)
  nxt_ctx: SearchContext = next_context(ctx, nxt_cell, sofar, ctx.letters)
  nxt_ctx.score += LETTERS[cell.value.lower()]
  return nxt_ctx, nxt_cell

def next_context(ctx: SearchContext, nxt_cell: Optional[Cell], sofar: str, letters: str) -> SearchContext:
  nxt_ctx = clone_context(ctx)
  nxt_ctx.grid = grid_copy(ctx.grid)
  nxt_ctx.sofar = sofar
  nxt_ctx.letters = letters
  nxt_ctx.is_anchored = ctx.is_anchored or (nxt_cell is not None and nxt_cell.is_anchored())
  return nxt_ctx

def is_word_boundary(cell: Optional[Cell]) -> bool:
  return cell is None or cell.value is None

def findwords(srch: SearchCriteria) -> Dict[str, int]:
  if srch.start_cell.value is not None:
    print("can't start a search from a cell that already has a value: "
          f"({srch.start_cell.pos.x},{srch.start_cell.pos.y})={srch.start_cell.value}")
    return {}

  is_anchored: bool = srch.start_cell.is_middle_cell()
  ctx: SearchContext = SearchContext(srch, is_anchored)
  strpath, _ = srch.grid.string(srch.start_cell, opposite(srch.dirn))
  ctx.sofar = strpath[::-1]
  return search(ctx, srch.start_cell, 0)


def unique_letters(letters: str) -> str:
  out: str = ""
  for ch in letters:
    if ch not in out:
      out += ch
  return out


def search(ctx: SearchContext, cell: Optional[Cell], depth: int) -> Dict[str, int]:
  # FIXME: probably should fix this to use FoundWord as key,
  # so that if we find the same english word in multiple
  # places we can report them all
  words: Dict[str, FoundWord] = {}
  if cell is not None:
    if cell.value is None:
      letters = ctx.letters
      for ch in unique_letters(letters):
        nxt_ctx, nxt_cell = add_letter(ctx, cell, ch, depth)
        # print(f"{'  ' * depth}{ctx.sofar} -> {nxt_ctx.sofar}       ({nxt_ctx.letters})")

        crosscheck, scoreadd = check_cross_direction(ctx, cell, ch)
        nxt_ctx.scoreadd += scoreadd
        # print(f"cross direction check for {ctx.sofar} + {ch} = {crosscheck}", flush=True)

        # fixme: probably should keep TrieNode so this check is O(1)
        tnode: Optional[TrieNode] = ctx.srch.trie.isprefix(nxt_ctx.sofar)
        if tnode is not None and crosscheck:
          if is_word_boundary(nxt_cell) and tnode.isword and ctx.is_anchored:
            addword(nxt_ctx, cell, words)
          rres = search(nxt_ctx, nxt_cell, depth+1)
          addwords(words, rres)

    else:
      nxt_ctx, nxt_cell = add_existing(ctx, cell)
      tnode: Optional[TrieNode] = ctx.srch.trie.isprefix(nxt_ctx.sofar)
      if tnode is not None:
        if is_word_boundary(nxt_cell) and tnode.isword:
          addword(nxt_ctx, cell, words)
        rres = search(nxt_ctx, nxt_cell, depth+1)
        addwords(words, rres)

  return words

def check_cross_direction(ctx: SearchContext, cell: Cell, letter: str) -> Tuple[bool, int]:
  match ctx.srch.dirn:
    case Dir.RIGHT:
      prefix, start = ctx.grid.upstr(cell)
      suffix, end = ctx.grid.downstr(cell)
    case Dir.DOWN:
      prefix, start = ctx.grid.leftstr(cell)
      suffix, end = ctx.grid.rightstr(cell)
    case _:
      raise Exception("cannot form words in leftward or upward directions")

  if start is None and end is None:
    return True, 0

  fullstr: str = prefix + letter + suffix
  tnode = ctx.srch.trie.isprefix(fullstr)
  if tnode is not None and tnode.isword:
    scoreadd: int = 0
    for ch in fullstr:
      scoreadd += LETTERS[ch.lower()]
    scoreadd *= cell.word_mult()
    scoreadd += LETTERS[letter.lower()] * (cell.letter_mult() - 1)
    return True, scoreadd

  return False, 0


def addword(ctx: SearchContext, cell: Cell, words: Dict[str, FoundWord]) -> None:
  score: int = ctx.score * ctx.scoremult + ctx.scoreadd
  pos: CPos = cell.pos.traverse(len(ctx.sofar) - 1, opposite(ctx.srch.dirn))
  words[ctx.sofar] = FoundWord(ctx.sofar, score, pos, ctx.srch.dirn)
  print(f"{words[ctx.sofar]} at ({pos.x},{pos.y})", flush=True)
  # print(ctx.grid.show() + "\n", flush=True)
  

def addwords(dest: Dict[str, FoundWord], src: Dict[str, FoundWord]) -> None:
  for k in src:
    if k not in dest or src[k].score > dest[k].score:
      dest[k] = src[k]
