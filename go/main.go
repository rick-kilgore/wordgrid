package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/derekparker/trie"
)

var (
	gamefile      *string
	wordsfile     *string
	sboard        *int
	pboard        *int
	pos           *string
	row           *int
	details_count *int
	bylen         *bool
	verbose       *bool
	showboard     *int
	letters       *string
)

func init() {
	gamefile = flag.String("f", "", "board represted by file as input")
	wordsfile = flag.String("w", "mix.txt", "use a different words file")
	sboard = flag.Int("sb", 0, "use one of the solo match grids (1-based index)")
	pboard = flag.Int("pb", 0, "specify a player board to use (1-based index)")
	pos = flag.String("p", "", "look for words starting at x,y pos")
	row = flag.Int("r", -1, "look for words starting in row N")
	details_count = flag.Int("d", 20, "number of detailed results to show")
	bylen = flag.Bool("l", false, "sort results by word length first")
	verbose = flag.Bool("v", false, "print some debugging info on console")
	showboard = flag.Int("s", -1, "show the tiles on board N")
}

func main() {
	flag.Parse()
	if *showboard > 0 {
		board := SoloBoards[*showboard]
		var grid *Grid = NewGrid(board)
		fmt.Println(grid.show())
		os.Exit(0)
	}
	var board BoardSpec = PlayerBoards[0]
	if *sboard > 0 {
		board = SoloBoards[*sboard]
	} else if *pboard > 0 {
		board = PlayerBoards[*pboard]
	}
	var grid *Grid = LoadBoard(board, *gamefile)
	if *verbose {
		fmt.Println(grid.show())
	}
	var trie *trie.Trie = LoadTrie(*wordsfile)
	var words map[string]FoundWord
	var letters string = flag.Args()[0]

	if *pos != "" {
		var x, y int
		fmt.Sscanf(*pos, "%d,%d", &x, &y)
		words = SearchFromSinglePos(*grid, trie, letters, x, y, *verbose)
	} else if *row >= 0 && *row < grid.h {
		words = SearchFromRow(*grid, trie, letters, *row, *verbose)
	} else {
		words = SearchWholeBoard(*grid, trie, letters, *verbose)
	}
	fmt.Println(DisplayResults(*grid, words, *details_count, *bylen))
}
