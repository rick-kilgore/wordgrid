package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type CPos struct {
	gridw, i, x, y int
}

func NewCPos(gridw, i int) CPos {
	return CPos{gridw, i, i % gridw, i / gridw}
}

func (pos CPos) String() string {
	return fmt.Sprintf("(%d,%d)", pos.x, pos.y)
}

// WARNING: this method assumes the caller knows
// what they are doing in that the requested
// traversal will not go off the board
func (pos CPos) Traverse(ncells int, dirn Dir) CPos {
	switch dirn {
	case UP:
		return NewCPos(pos.gridw, pos.i-(pos.gridw*ncells))
	case DOWN:
		return NewCPos(pos.gridw, pos.i+(pos.gridw*ncells))
	case LEFT:
		return NewCPos(pos.gridw, pos.i-ncells)
	case RIGHT:
		return NewCPos(pos.gridw, pos.i+ncells)
	default:
		return pos
	}
}

type Cell struct {
	pos   CPos
	ctype string
	value string
	added bool
}

func (cell Cell) String() string {
	val := cell.value
	if val == "" {
		switch cell.ctype {
		case BLANK:
			val = ""
		default:
			val = cell.ctype
		}
	}
	return fmt.Sprintf("%s:%s", cell.pos, val)
}

func (cell Cell) LetterMult() int {
	switch cell.ctype {
	case DL:
		return 2
	case TL:
		return 3
	default:
		return 1
	}
}

func (cell Cell) WordMult() int {
	switch cell.ctype {
	case DW:
		return 2
	case TW:
		return 3
	default:
		return 1
	}
}

type Grid struct {
	w, h  int
	tiles []RowSpec
	cells []Cell
}

func NewGrid(board BoardSpec) *Grid {
	newgrid := &Grid{board.w, board.h, board.tiles, make([]Cell, board.w*board.h)}
	for nrow := 0; nrow < newgrid.h; nrow++ {
		var srcrow int = nrow
		if nrow >= len(newgrid.tiles) {
			srcrow = newgrid.h - 1 - nrow
		}
		var row RowSpec = newgrid.tiles[srcrow]
		for ncol := 0; ncol < newgrid.w; ncol++ {
			pos := NewCPos(newgrid.w, nrow*newgrid.w+ncol)
			ctype := row[ncol]
			if ctype == "" {
				ctype = BLANK
			}
			newgrid.cells[pos.i] = Cell{pos, ctype, "", false}
		}
	}

	if newgrid.board_has_unknowns(board) {
		print("[33;mThis board has unknowns![m")
		print("\n", newgrid.show())
		Input("\nHit return to continue")
	}

	return newgrid
}

func (g Grid) board_has_unknowns(board BoardSpec) bool {
	for _, row := range board.tiles {
		for _, ctype := range row {
			if ctype == UK {
				return true
			}
		}
	}
	return false
}

func (g Grid) at(x, y int) *Cell {
	return &g.cells[g.w*y+x]
}

func (g Grid) Serialize() string {
	str := fmt.Sprintf("%d:%d", g.w, g.h)
	for _, cell := range g.cells {
		if cell.value != "" {
			str += cell.value
		} else {
			switch cell.ctype {
			case BLANK:
				str += " "
			case DL:
				str += "-"
			case TL:
				str += "_"
			case DW:
				str += "="
			case TW:
				str += "+"
			}
		}
	}
	return str
}

func deserialize(str string) *Grid {
	var split []string = strings.Split(str, ":")
	sw, sh, data := split[0], split[1], split[2]
	w, err := strconv.Atoi(sw)
	h, err2 := strconv.Atoi(sh)
	if err != nil || err2 != nil {
		fmt.Fprintf(os.Stderr, "bad width or height string: w=%s h=%s\n", sw, sh)
		return nil
	}
	grid := NewGrid(BoardSpec{w, h, []RowSpec{}})
	for i, ch := range data {
		pos := NewCPos(grid.w, i)
		switch ch {
		case ' ':
			grid.cells[i] = Cell{pos, BLANK, "", false}
		case '-':
			grid.cells[i] = Cell{pos, DL, "", false}
		case '_':
			grid.cells[i] = Cell{pos, TL, "", false}
		case '=':
			grid.cells[i] = Cell{pos, DW, "", false}
		case '+':
			grid.cells[i] = Cell{pos, TW, "", false}
		default:
			grid.cells[i] = Cell{pos, BLANK, string(ch), false}
		}
	}
	return grid
}

func (g Grid) clone() Grid {
	newgrid := Grid{g.w, g.h, g.tiles, make([]Cell, g.w*g.h)}
	for i, cell := range g.cells {
		newgrid.cells[i] = Cell{cell.pos, cell.ctype, cell.value, cell.added}
	}
	return newgrid
}

func (g Grid) show() string {
	showstr := "   "
	for i := 0; i < g.w; i++ {
		showstr += fmt.Sprintf("%2s ", strconv.Itoa(i))
	}
	showstr += "\n"
	for y := 0; y < g.h; y++ {
		showstr += fmt.Sprintf("%2s ", strconv.Itoa(y))
		for x := 0; x < g.w; x++ {
			cell := g.at(x, y)
			if cell.value != "" {
				esc := 34
				if cell.added {
					esc = 32
				}
				showstr += fmt.Sprintf(" [1;%dm%s[m ", esc, cell.value)
			} else {
				showstr += fmt.Sprintf(" %s", g.at(x, y).ctype)
			}
		}
		showstr += "\n"
	}

	return showstr
}

// color the found word based on which letters are being added and which
// were already there
func (g Grid) ColorWord(word string, startpos CPos, dirn Dir) (string, error) {
	pos := startpos
	inEsc := false
	coloredStr := ""
	for _, ch := range word {
		cell := g.at(pos.x, pos.y)
		var letter2apply string = string(ch)
		if cell.value == "" {
			if !inEsc {
				coloredStr += "\x1b[1;32m"
				inEsc = true
			}
			coloredStr += letter2apply

		} else if cell.value == letter2apply {
			if inEsc {
				coloredStr += "\x1b[m"
				inEsc = false
			}
			coloredStr += letter2apply

		} else {
			msg := fmt.Sprintf("could not apply %s at %s dir %s to:\n%s",
				word, startpos, dirn, g.show())
			msg += fmt.Sprintf("failure applying word %s: found existing letter %s "+
				"at (%d,%d) instead of '%s'",
				word, cell.value, pos.x, pos.y, letter2apply)
			fmt.Println(msg)
			return "", errors.New(msg)
		}
		pos = pos.Traverse(1, dirn)
	}
	if inEsc {
		coloredStr += "\x1b[m"
	}

	return coloredStr, nil
}

func (g *Grid) apply(word string, startpos CPos, dirn Dir) (*Grid, error) {
	grid := g.clone()
	pos := startpos
	for _, ch := range word {
		cell := grid.at(pos.x, pos.y)
		var letter2apply string = string(ch)
		if cell.value == "" {
			cell.value = letter2apply
			cell.added = true
		} else if cell.value != letter2apply {
			msg := fmt.Sprintf("could not apply %s at %s dir %s to:\n%s",
				word, startpos, dirn, g.show())
			msg += fmt.Sprintf("failure applying word %s: found existing letter %s "+
				"at (%d,%d) instead of '%s'",
				word, cell.value, pos.x, pos.y, letter2apply)
			fmt.Println(msg)
			return nil, errors.New(msg)
		}
		pos = pos.Traverse(1, dirn)
	}

	return &grid, nil
}

func (g Grid) next_cell(cell Cell, dirn Dir) *Cell {
	var next *Cell
	switch dirn {
	case UP:
		next = g.up_from(cell)
	case DOWN:
		next = g.down_from(cell)
	case LEFT:
		next = g.left_from(cell)
	case RIGHT:
		next = g.right_from(cell)
	default:
		panic(fmt.Sprintf("unrecognized direction: %s", dirn))
	}
	return next
}

func (g Grid) left_from(cell Cell) *Cell {
	if cell.pos.x == 0 {
		return nil
	}
	return &g.cells[cell.pos.i-1]
}

func (g Grid) right_from(cell Cell) *Cell {
	if cell.pos.x >= g.w-1 {
		return nil
	}
	return &g.cells[cell.pos.i+1]
}

func (g Grid) up_from(cell Cell) *Cell {
	if cell.pos.y == 0 {
		return nil
	}
	return &g.cells[cell.pos.i-g.w]
}

func (g Grid) down_from(cell Cell) *Cell {
	if cell.pos.y >= g.h-1 {
		return nil
	}
	if cell.pos.i+g.w >= len(g.cells) {
		fmt.Printf("down_from failing: from cell=%v", cell)
	}
	return &g.cells[cell.pos.i+g.w]
}

func (g Grid) StrUpFromCell(cell Cell) (str string, end_cell *Cell) {
	strpath, start := g.StrFromCell(cell, UP)
	return Reverse(strpath), start
}

func (g Grid) StrDownFromCell(cell Cell) (str string, end_cell *Cell) {
	return g.StrFromCell(cell, DOWN)
}

func (g Grid) StrLeftFromCell(cell Cell) (str string, end_cell *Cell) {
	strpath, start := g.StrFromCell(cell, LEFT)
	return Reverse(strpath), start
}

func (g Grid) StrRightFromCell(cell Cell) (str string, end_cell *Cell) {
	return g.StrFromCell(cell, RIGHT)
}

// string of all letters between the passed-in cell in direction
// dirn, up to the first blank cell or edge of the board.
func (g Grid) StrFromCell(cell Cell, dirn Dir) (str string, end_cell *Cell) {
	str = ""
	end_cell = nil
	var nxt *Cell = g.next_cell(cell, dirn)
	for nxt != nil && nxt.value != "" {
		str += nxt.value
		end_cell = nxt
		nxt = g.next_cell(*nxt, dirn)
	}
	return
}

func (g Grid) IsMiddleCell(cell Cell) bool {
	return cell.pos.x == g.w/2 && cell.pos.y == g.h/2
}

func (g Grid) IsAnchored(cell Cell) bool {
	var up *Cell = g.up_from(cell)
	var down *Cell = g.down_from(cell)
	var left *Cell = g.left_from(cell)
	var right *Cell = g.right_from(cell)
	return ((up != nil && up.value != "" && !up.added) ||
		(down != nil && down.value != "" && !down.added) ||
		(left != nil && left.value != "" && !left.added) ||
		(right != nil && right.value != "" && !right.added))
}

func GridFromFile(fname string, board BoardSpec) *Grid {
	grid := NewGrid(board)

	data, err := os.ReadFile(fname)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to read grid state from %s\n", fname)
	}
	var rows []string = strings.Split(string(data), "\n")
	var line int = 0
	for line < grid.h {
		var row string = strings.Trim(rows[line], " \r\n")
		for i, ch := range row {
			if ch != '-' && ch != ' ' {
				grid.at(i, line).value = string(ch)
			}
		}
		line += 1
	}
	return grid
}
