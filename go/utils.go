package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"sort"
	"strings"

	"github.com/derekparker/trie"
)

// Interfaces used for testing
type (
	Reader interface {
		ReadString(delim byte) (string, error)
	}
	Scanner interface {
		Scan() bool
		Text() string
	}
	File interface {
		Close() error
	}
	RFac    func(rd io.Reader) Reader
	SFac    func(f File) Scanner
	FOpener func(fname string) (File, error)
)

var (
	ReaderFactory  RFac    = func(rd io.Reader) Reader { return bufio.NewReader(rd) }
	ScannerFactory SFac    = func(f File) Scanner { return bufio.NewScanner(f.(*os.File)) }
	FileOpener     FOpener = func(fname string) (File, error) { return os.Open(fname) }
)

// end Interfaces used for testing

func Log(srch *SearchCriteria, msg string) {
	if srch.verbose {
		fmt.Print(msg)
	}
}

func Spaces(n int) string {
	if n < 0 {
		return ""
	}
	spcs := make([]rune, n)
	for i := 0; i < n; i++ {
		spcs[i] = ' '
	}
	return string(spcs)
}

func Reverse(str string) string {
	in := []rune(str)
	strlen := len(in)
	out := make([]rune, strlen)
	for i := 0; i < strlen; i++ {
		out[i] = in[strlen-1-i]
	}
	return string(out)
}

func Input(prompt string) string {
	var reader Reader = ReaderFactory(os.Stdin)
	fmt.Printf("%s: ", prompt)
	text, _ := reader.ReadString('\n')
	return text
}

func LoadBoard(board BoardSpec, file string) *Grid {
	return GridFromFile(file, board)
}

func LoadTrie(words_file string) *trie.Trie {
	fmt.Printf("loading words from %s\n", words_file)
	dictwords := trie.New()
	file, err := FileOpener(words_file)
	if err != nil {
		panic(fmt.Sprintf("failed to open words file %s: %v\n", words_file, err))
	}
	scanner := ScannerFactory(file)
	for scanner.Scan() {
		dictwords.Add(strings.ToLower(strings.Trim(scanner.Text(), " \r\n")), 1)
	}

	file.Close()
	return dictwords
}

func MapKeys(themap map[string]FoundWord) []string {
	keys := make([]string, 0, len(themap))
	for k := range themap {
		keys = append(keys, k)
	}
	return keys
}

func MapValues(themap map[string]FoundWord) []interface{} {
	vals := make([]interface{}, 0, len(themap))
	for _, v := range themap {
		vals = append(vals, v)
	}
	return vals
}

func DisplayResults(grid Grid, words map[string]FoundWord, details_count int, sortbylen bool) string {

	var keys []string = MapKeys(words)

	less := func(i, j int) bool {
		ki, kj := keys[i], keys[j]
		if sortbylen {
			if words[ki].used != words[kj].used {
				return words[ki].used < words[kj].used
			}
			return words[ki].score < words[kj].score

		} else if words[ki].score != words[kj].score {
			return words[ki].score < words[kj].score
		}
		return words[ki].used < words[kj].used
	}

	sort.Slice(keys, less)
	var disp_str string = "found:"
	for _, k := range keys {
		disp_str += fmt.Sprintf("\n  %s", words[k].AsResult(grid))
	}
	disp_str += "\n"

	if details_count > len(keys) {
		details_count = len(keys)
	}

	if details_count > 0 {
		disp_str += fmt.Sprintf("\n\ntop %d are:\n\n", details_count)
		for d := details_count; d > 0; d-- {
			i := len(keys) - d
			var fw FoundWord = words[keys[i]]
			disp_str += fmt.Sprintf("%02d: %s\n", d, fw)
			gcl, err := grid.apply(fw.word, fw.pos, fw.dirn)
			if err != nil {
				fmt.Printf("failure applying %s: %v\n", fw.word, err)
			} else {
				disp_str += gcl.show() + "\n"
			}
		}
	}

	return disp_str
}
