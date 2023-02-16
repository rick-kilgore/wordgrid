package main

import (
  "bufio"
  "fmt"
  "os"
  "sort"
  "strings"
  "github.com/derekparker/trie"
)

func Reverse(str string) string {
  in := []rune(str)
  strlen := len(in)
  out := make([]rune, strlen)
  for i := 0; i < strlen; i++ {
    out[i] = in[strlen - 1 - i]
  }
  return string(out)
}

func LoadBoard(board_num int, file string) Grid {
  width, height, bspec := GetBoardData(board_num)
  return GridFromFile(file, width, height, bspec)
}


func LoadTrie(words_file string) *trie.Trie {
  dictwords := trie.New()
  file, err := os.Open(words_file)
  if err != nil {
    panic(fmt.Sprintf("failed to open words file %s: %v\n", words_file, err))
  }
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    dictwords.Add(strings.ToLower(strings.Trim(scanner.Text(), " \r\n")), 1)
  }

  file.Close()
  return dictwords
}


func MapKeys(themap map[string]FoundWord) []string {
  keys := make([]string, 0, len(themap))
  for k, _ := range themap {
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
    ri, rj := []rune(ki), []rune(kj)
    if sortbylen {
      if len(ri) != len(rj) {
        return len(ri) < len(rj)
      }
      return words[ki].score < words[kj].score

    } else if words[ki].score != words[kj].score {
      return words[ki].score < words[kj].score
    }
    return len(ri) < len(rj)
  }

  sort.Slice(keys, less)
  var disp_str string = "found:"
  for _, fw := range words {
    disp_str += "\n  " + fw.Str()
  }
  disp_str += "\n"

  if details_count > 0 {
    disp_str += fmt.Sprintf("\n\ntop %d are:\n\n", details_count)
    for i := len(keys) - details_count; i < len(keys); i++ {
      var fw FoundWord = words[keys[i]]
      disp_str += fmt.Sprintf("%02s: %s\n", details_count - i, fw.Str())
      var gcl Grid = grid.clone()
      gcl.apply(fw.word, fw.pos, fw.dirn)
      disp_str += gcl.show() + "\n"
    }
  }

  return disp_str
}
