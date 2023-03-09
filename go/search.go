package main

import (
  "fmt"
  "strings"
  "github.com/derekparker/trie"
)

type SearchCriteria struct {
  grid Grid
  start_cell Cell
  dirn Dir
  letters string
  trie *trie.Trie
  verbose bool
}

func (sc SearchCriteria) String() string {
  return fmt.Sprintf("[search: start=%s dir=%s letters=%s]",
                     sc.start_cell, sc.dirn, sc.letters)
}

type SearchContext struct {
  srch *SearchCriteria
  grid *Grid
  cell *Cell
  letters string
  used int
  sofar string
  score int
  scoreadd, scoremult int
  is_anchored bool
}

func NewSearchContext(srch *SearchCriteria, is_anchored bool) SearchContext {
  return SearchContext{
      srch, &srch.grid, &srch.start_cell, srch.letters,
      0,  // used
      "", // sofar
      0,  // score
      0,  // scoreadd
      1,  // scoremult
      is_anchored,
  }
}


func (sc SearchContext) String() string {
  return fmt.Sprintf("[ctx: %s cell=%s dir=%s letters=%s sofar=%s]",
                     *sc.srch, *sc.cell, sc.srch.dirn, sc.letters, sc.sofar)
}


func clone_context(ctx *SearchContext) SearchContext {
  return SearchContext{
    ctx.srch, ctx.grid, ctx.cell,
    ctx.letters, ctx.used, ctx.sofar,
    ctx.score, ctx.scoreadd, ctx.scoremult,
    ctx.is_anchored,
  }
}

type FoundWord struct {
  word string
  score int
  used int
  pos CPos
  dirn Dir
}

/*
  def __init__(self, word: str, score: int, pos: CPos, dirn: Dir):
    self.word = word
    self.score = score
    self.pos = pos
    self.dirn = dirn
*/

func (fw FoundWord) String() string {
  return fmt.Sprintf("%d: %s %s from %s (%d ltrs)", fw.score, fw.word, fw.dirn, fw.pos, fw.used)
}


// ctx contains the Cell to which we are adding the letter
// the returned nxt_ctx points to the next Cell in the search direction
// ltr and ch will be the same except in the case where ltr == '.' and ch any letter
//    of the alphabet we are adding to the search to fulfill this wildcard
func add_letter(ctx *SearchContext, cell Cell, ltr string, ch string, depth int) (SearchContext, *Cell) {
  var sofar string = ctx.sofar + string(ch)
  var letters string = strings.Replace(ctx.letters, ltr, "", 1)
  var nxt_cell *Cell = ctx.grid.next_cell(cell, ctx.srch.dirn)
  var nxt_ctx SearchContext = next_context(ctx, cell, sofar, letters)
  nxt_ctx.used++
  scoreadd := 0
  if ch == ltr {
    letval := LETTERS[strings.ToLower(ch)]
    mult := cell.LetterMult()
    scoreadd = letval * mult
    nxt_ctx.score += scoreadd
  }
  Log(ctx.srch, fmt.Sprintf("%sat %s dir=%s - sofar=%s: add score %d -> %d\n",
                            Spaces(depth * 2), cell, ctx.srch.dirn, sofar, scoreadd, nxt_ctx.score))
  nxt_ctx.scoremult *= cell.WordMult()
  return nxt_ctx, nxt_cell
}

// ctx contains the Cell with the letter we are adding to sofar
// the returned nxt_ctx points to the next Cell in the search direction
func add_existing(ctx *SearchContext, cell Cell, depth int) (SearchContext, *Cell) {
  var sofar string = ctx.sofar + cell.value
  var nxt_cell *Cell = ctx.grid.next_cell(cell, ctx.srch.dirn)
  var nxt_ctx SearchContext = next_context(ctx, cell, sofar, ctx.letters)
  scoreadd := LETTERS[strings.ToLower(cell.value)]
  nxt_ctx.score += scoreadd
  Log(ctx.srch, fmt.Sprintf("%sat %s dir=%s - sofar=%s: add score %d -> %d\n",
                            Spaces(depth * 2), cell, ctx.srch.dirn, sofar, scoreadd, nxt_ctx.score))
  return nxt_ctx, nxt_cell
}

func next_context(ctx *SearchContext, cell Cell, sofar string, letters string) SearchContext {
  var nxt_ctx SearchContext = clone_context(ctx)
  nxt_ctx.sofar = sofar
  nxt_ctx.letters = letters
  now_anchored := ctx.grid.IsAnchored(cell)
  if !ctx.is_anchored && now_anchored {
    ctx.is_anchored = true
  }
  nxt_ctx.is_anchored = ctx.is_anchored
  return nxt_ctx
}

func is_word_boundary(cell *Cell) bool {
  return cell == nil || cell.value == ""
}

func Findwords(srch *SearchCriteria) map[string]FoundWord {
  if srch.start_cell.value != "" {
    Log(srch, fmt.Sprintf("can't start a search from a cell that already has a value: (%d,%d)=%s",
                          srch.start_cell.pos.x, srch.start_cell.pos.y, srch.start_cell.value))
    return map[string]FoundWord{}
  }

  var is_anchored bool = srch.grid.IsMiddleCell(srch.start_cell) || srch.grid.IsAnchored(srch.start_cell)
  var ctx SearchContext = NewSearchContext(srch, is_anchored)
  strpath, _ := srch.grid.StrFromCell(srch.start_cell, Opposite(srch.dirn))
  for _, ch := range strpath {
    ctx.score += LETTERS[strings.ToLower(string(ch))]
  }
  ctx.sofar = Reverse(strpath)
  return search(ctx, &srch.start_cell, 0)
}


func unique_letters(letters string) string {
  var out string = ""
  for _, ch := range letters {
    s := string(ch)
    if !strings.Contains(out, s) {
      out += s
    }
  }
  return out
}


func search(ctx SearchContext, cell *Cell, depth int) map[string]FoundWord {
  // TODO: probably should fix this to use FoundWord as key
  // so that if we find the same english word in multiple
  // places we can report them all
  words := map[string]FoundWord{}
  if cell != nil {
    if cell.value == "" {
      var letters string = ctx.letters
      for _, ltrRune := range unique_letters(letters) {
        ltr := string(ltrRune)
        var chars string = ltr
        if ltr == "." {
          chars = "abcdefghijklmnopqrstuvwxyz"
        }
        for _, ch := range chars {
          s := string(ch)
          nxt_ctx, nxt_cell := add_letter(&ctx, *cell, ltr, s, depth)

          crosscheck, scoreadd := check_cross_direction(ctx, *cell, ltr, s)
          if scoreadd > 0 {
            Log(ctx.srch, fmt.Sprintf("%sadding %d from crosscheck at %s\n", Spaces(depth*2), scoreadd, cell.pos))
          }
          nxt_ctx.scoreadd += scoreadd

          var isprefix bool = ctx.srch.trie.HasKeysWithPrefix(nxt_ctx.sofar)
          if isprefix && crosscheck {
            node, _ := ctx.srch.trie.Find(nxt_ctx.sofar)
            if is_word_boundary(nxt_cell) && node != nil && ctx.is_anchored {
              addword(nxt_ctx, *cell, words, depth)
            }
            var rres map[string]FoundWord = search(nxt_ctx, nxt_cell, depth+1)
            addwords(words, rres)
          }
        }
      }

    } else {
      nxt_ctx, nxt_cell := add_existing(&ctx, *cell, depth)
      var isprefix bool = ctx.srch.trie.HasKeysWithPrefix(nxt_ctx.sofar)
      if isprefix {
        node, _ := ctx.srch.trie.Find(nxt_ctx.sofar)
        if is_word_boundary(nxt_cell) && node != nil {
          addword(nxt_ctx, *cell, words, depth)
        }
        var rres map[string]FoundWord = search(nxt_ctx, nxt_cell, depth+1)
        addwords(words, rres)
      }
    }
  }
  return words
}


// ltr and ch will be the same except in the case where ltr == '.' and ch any letter
//    of the alphabet we are adding to the search to fulfill this wildcard
func check_cross_direction(ctx SearchContext, cell Cell, ltr string, ch string) (bool, int) {
  var prefix, suffix string
  var start, end *Cell

  switch ctx.srch.dirn {
    case RIGHT:
      prefix, start = ctx.grid.StrUpFromCell(cell)
      suffix, end = ctx.grid.StrDownFromCell(cell)
    case DOWN:
      prefix, start = ctx.grid.StrLeftFromCell(cell)
      suffix, end = ctx.grid.StrRightFromCell(cell)
    default:
      panic("cannot form words in leftward or upward directions")
  }

  if start == nil && end == nil {
    return true, 0
  }

  var fullstr string = prefix + ch + suffix
  node, _ := ctx.srch.trie.Find(fullstr)
  if node != nil {
    scoreadd := 0
    for _, crossch := range string(prefix + suffix) {
      scoreadd += LETTERS[strings.ToLower(string(crossch))]
    }
    scoreadd *= cell.WordMult()
    if ltr == ch {
      scoreadd += LETTERS[strings.ToLower(ch)] * cell.LetterMult() * cell.WordMult()
    }
    return true, scoreadd
  }

  // isword == false
  return false, 0
}


func addword(ctx SearchContext, cell Cell, words map[string]FoundWord, depth int) {
  score := 0
  wlen := len([]rune(ctx.sofar))
  if wlen == 1 {
    score = ctx.scoreadd
  } else {
    score = ctx.score * ctx.scoremult + ctx.scoreadd
  }
  if ctx.used == 7 {
    score += 35
  }
  var pos CPos = cell.pos.Traverse(wlen - 1, Opposite(ctx.srch.dirn))
  prev, exists := words[ctx.sofar]
  if !exists || prev.score < score {
    words[ctx.sofar] = FoundWord{ctx.sofar, score, ctx.used, pos, ctx.srch.dirn}
  }
  Log(ctx.srch, fmt.Sprintf("%saddword: %s\n", Spaces(depth * 2), words[ctx.sofar]))
}


func addwords(dest map[string]FoundWord, src map[string]FoundWord) {
  for k, v := range src {
    prev, exists := dest[k]
    if !exists || v.score > prev.score {
      dest[k] = v
    }
  }
}

func SearchFromSinglePos(
    grid Grid,
    trie *trie.Trie,
    letters string,
    startx int,
    starty int,
    verbose bool,
) map[string]FoundWord {
  if verbose {
    fmt.Printf("searching from (%d,%d)\n", startx, starty)
  }
  words := map[string]FoundWord{}
  if startx >= 0 && startx < grid.w - 1 {
    srch := SearchCriteria{grid, *grid.at(startx, starty), RIGHT, letters, trie, verbose}
    words = Findwords(&srch)
  }
  if starty >= 0 && starty < grid.h - 1 {
    srch := SearchCriteria{grid, *grid.at(startx, starty), DOWN, letters, trie, verbose}
    addwords(words, Findwords(&srch))
  }
  return words
}


func SearchFromRow(grid Grid, trie *trie.Trie, letters string, nrow int, verbose bool) map[string]FoundWord {
  words := map[string]FoundWord{}
  for x := 0; x < grid.w; x++ {
    var cell *Cell = grid.at(x, nrow)
    if cell.value == "" {
      addwords(words, SearchFromSinglePos(grid, trie, letters, x, nrow, verbose))
    }
  }
  return words
}


func SearchWholeBoard(grid Grid, trie *trie.Trie, letters string, verbose bool) map[string]FoundWord {
  words := map[string]FoundWord{}
  for y := 0; y < grid.h; y++ {
    for x := 0; x < grid.w; x++ {
      var cell *Cell = grid.at(x, y)
      if cell.value == "" {
        rres := SearchFromSinglePos(grid, trie, letters, x, y, verbose)
        addwords(words, rres)
      }
    }
  }
  return words
}
