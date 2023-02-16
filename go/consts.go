package main

import (
  "fmt"
)


const (
  BLANK string = "__"
  DL string = "DL"
  TL string = "TL"
  DW string = "DW"
  TW string = "TW"
  UK string = "??"
)

const (
  GWIDTH int = 15
  GHEIGHT int = 15
  SOLO_WIDTH int = 11
  SOLO_HEIGHT int = 11
)

type RowSpec map[int]string
type BoardSpec []RowSpec

// board used against other players
var player_board = BoardSpec{
  { 3: TW, 6: TL, 8: TL, 11: TW, },
  { 2: DL, 5: DW, 9: DW, 12: DL, },
  { 1: DL, 4: DL, 10: DL, 13: DL, },
  { 0: TW, 3: TL, 7: DW, 11: TL, 14: TW, },
  { 2: DL, 6: DL, 8: DL, 12: DL, },
  { 1: DW, 5: TL, 9: TL, 13: DW, },
  { 0: TL, 4: DL, 10: DL, 14: TL, },
  { 3: DW, 11: DW, },
}

// 1st solo challenge board
var board1 = BoardSpec{
  { 0: TL, 2: TW, 8: TW, 10: TL, },
  { 1: DW, 5: DW, 9: DW, },
  { 0: TW, 2: DL, 4: DL, 6: DL, 8: DL, 10: TW, },
  { 3: TL, 7: TL, },
  { 2: DL, 8: DL, },
  { 1: DW, 9: DW, },
}

// 2nd solo challenge board
var board2 = BoardSpec{
  { 0: TW, 3: DL, 4: TL, 7: DL, 8: TW, },
  { 0: DL, 1: DW, 4: DL, 5: DL, 8: DL, 9: DW, },
  { 1: DL, 2: TW, 5: DL, 6: TL, 9: DL, 10: TW, },
  { 2: DL, 3: DW, 6: DL, 7: DW, 10: DL, },
  { 0: DL, 3: DL, 4: DL, 7: DL, 8: DL, },
  { 0: TL, 1: DL, 4: DL, },
}

// 3rd solo challenge board
var board3 = BoardSpec{
  { 0: TW, 4: DL, 5: DL, 6: DL, 10: TW, },
  { 1: DW, 3: DL, 4: DL, 5: DL, 6: DL, 7: DL, 9: DW, },
  { 2: DL, 3: DL, 7: DL, 8: DL, },
  { 0: TL, 2: DL, 8: DL, 10: TL, },
  { 1: TL, 2: DL, 4: DL, 6: DL, 8: DL, 9: TL, },
  { 2: DL, 8: DL, },
  { 1: TL, 3: DL, 7: DL, 9: TL, },
  { 0: TL, 4: DL, 5: DL, 6: DL, 10: TL, },
  { 2: DW, 4: DL, 6: DL, 9: DW, },
  { 1: TL, 4: DL, 6: DL, 9: TL, },
  { 0: TW, 5: TL, 10: TW, },
}

// 4th solo challenge board
var board4 = BoardSpec{
  { 0: TW, 1: DL, 2: DL, 5: TL, 8: DL, 9: DL, 10: TW, },
  { 0: DL, 1: DL, 4: DL, 5: DL, 6: DL, 9: DL, 10: DL, },
  { 0: DL, 2: DW, 4: DL, 6: DL, 8: DW, 10: DL, },
  { },
  { 1: DL, 2: DL, 4: DL, 6: DL, 8: DL, 9: DL, },
  { 0: TL, 1: DL, 9: DL, 10: TL, },
}

// 5th solo challenge board
var board5 = BoardSpec{
  { 5: DW, },
  { 1: TW, 4: DL, 6: DL, 9: TW, },
  { 2: TL, 3: DL, 4: DL, 6: DL, 7: DL, 8: TL, },
  { 2: DL, 5: DL, 8: DL, },
  { 1: DL, 2: DL, 4: DL, 6: DL, 8: DL, 9: DL, },
  { 0: DW, 3: DL, 7: DL, 10: DW, },
}

// 6th solo challenge board
var board6 = BoardSpec{
  { 0: TW, 5: TW, 10: TW },
  { 1: DW, 3: TL, 5: DL, 7: TL, 9: DW },
  { 2: TL, 4: DL, 6: DL, 8: TL },
  { 1: TL, 3: DW, 5: DL, 7: DW, 9: TL },
  { 2: DL, 4: DL, 6: DL, 8: DL },
  { 0: TW, 1: DL, 3: DL, 7: DL, 9: DL, 10: TW },
}

// 7th solo challenge board
var board7 = BoardSpec{
  { 0: TW, 1: DL, 5: DL, 9: DL, 10: TW },
  { 0: DL, 1: DL, 2: DL, 5: TL, 8: DL, 9: DL, 10: DL },
  { 1: DL, 2: DW, 4: DL, 6: DL, 8: DW,  9: DL },
  { 3: DL, 4: TL, 6: TL, 7: DL },
  { 2: DL, 3: TL, 7: TL, 8: DL },
  { 0: DL, 1: TL, 9: TL, 10: DL },
}

// 8th solo challenge board
var board8 = BoardSpec{
  { 0: TW, 1: DL, 2: DL, 8: DL, 9: DL, 10: TW },
  { 0: DL, 3: TL, 7: TL, 10: DL },
  { 0: DL, 2: DW, 4: DL, 6: DL, 8: DW, 10: DL },
  { 0: DL, 5: UK, 10: DL },
  { 1: DL, 2: TL, 3: DL, 5: UK, 7: DL, 8: TL, 9: DL },
  { 4: DL, 5: UK, 6: DL },
  { 3: TL, 5: UK, 7: TL },
  { 2: DL, 5: UK, 8: DL },
  { 1: DL, 3: DL, 5: DW, 7: DL, 9: DL },
  { 1: TW, 4: DL, 6: DL, 9: TW },
  { 2: DL, 3: DL, 4: DL, 6: DL, 7: DL, 8: DL },
}

var Boards = []BoardSpec{
  player_board,
  board1,
  board2,
  board3,
  board4,
  board5,
  board6,
  board7,
  board8,
}

// returns [grid_width, grid_height, grid_spec]
func GetBoardData(board_num int) (int, int, BoardSpec) {
  var width, height int

  if board_num == 0 {
    width = GWIDTH
    height = GHEIGHT
  } else {
    width = SOLO_WIDTH
    height = SOLO_HEIGHT
  }
  return width, height, Boards[board_num]
}


type Dir int8
const (
  NODIR Dir = 0
  UP Dir = 1
  RIGHT Dir = 2
  DOWN Dir = 3
  LEFT Dir = 4
)

func (dir Dir) String() string {
  switch dir {
    case UP: return "UP"
    case RIGHT: return "RIGHT"
    case DOWN: return "DOWN"
    case LEFT: return "LEFT"
    default: return "UNKNOWN"
  }
}


func Opposite(dirn Dir) Dir {
  switch dirn {
    case UP:
      return DOWN
    case DOWN:
      return UP
    case LEFT:
      return RIGHT
    case RIGHT:
      return LEFT
    default:
      panic(fmt.Sprintf("unrecognized direction: %s", dirn))
  }
}

var LETTERS = map[string]int {
  "a": 1,
  "b": 4,
  "c": 4,
  "d": 2,
  "e": 1,
  "f": 4,
  "g": 3,
  "h": 3,
  "i": 1,
  "j": 10,
  "k": 5,
  "l": 2,
  "m": 4,
  "n": 2,
  "o": 1,
  "p": 4,
  "q": 10,
  "r": 1,
  "s": 1,
  "t": 1,
  "u": 2,
  "v": 5,
  "w": 4,
  "x": 8,
  "y": 3,
  "z": 10,
}
