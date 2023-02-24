package main

import (
  "fmt"
  "testing"
)

func TestSpaces(t *testing.T) {
  cases := map[int]string{
    1: " ", 5: "     ", 0: "", -1: "",
  }

  for n, exp := range cases {
    res := Spaces(n)
    fmt.Printf("TestSpaces(%d) -> \"%s\"\n", n, res)
    if res != exp {
      t.Errorf("Spaces(%d) = %s; expected %s", n, res, exp)
    }
  }
}

func TestReverse(t *testing.T) {
  cases := map[string]string{
    "hello": "olleh", "eye": "eye" , "": "", "be the ball": "llab eht eb",
  }
  for str, exp := range cases {
    rev := Reverse(str)
    fmt.Printf("TestReverse(\"%s\") -> \"%s\"\n", str, rev)
    if rev != exp {
      t.Errorf("Reverse(%s) = %s; expected %s", str, rev, exp)
    }
  }
}

type mockscanner struct {
  words []string
  nword int
}
func (ms *mockscanner) Scan() bool { ms.nword++; return ms.nword % len(ms.words) != len(ms.words) - 1 }
func (ms *mockscanner) Text() string { return ms.words[ms.nword % len(ms.words)] }

type mockfile struct {}
func (mf mockfile) Close() error { return nil }

func TestLoadTrie(t *testing.T) {
  // setup
  FileOpener = func(fname string) (File, error) {
    return mockfile{}, nil
  }
  ScannerFactory = func(f File) Scanner {
    return &mockscanner{[]string{ "abc", "ab", "nice", "nicer" }, -1}
  }

  // run test
  trie := LoadTrie("fakename")

  // verify stuff
  tofind := "nice"
  node, ok := trie.Find(tofind)
  fmt.Printf("trie.Find(\"%s\") = %v\n", tofind, ok)
  if !ok {
    t.Errorf("trie.Find(\"%s\") is nil: expected non-nil", tofind)
  }
  tofind = "foobar"
  node, ok = trie.Find(tofind)
  fmt.Printf("trie.Find(\"%s\") = %v\n", tofind, ok)
  if ok {
    t.Errorf("trie.Find(\"%s\") = %v: expected nil", tofind, node)
  }

  for _, tofind := range []string{"ni", "nice", "a"} {
    isprefix := trie.HasKeysWithPrefix(tofind)
    fmt.Printf("trie.HasKeysWithPrefix(\"%s\") = %v\n", tofind, isprefix)
    if !isprefix {
      t.Errorf("trie.HasKeysWithPrefix(\"%s\") = false: expected true", tofind)
    }
  }
  for _, tofind := range []string{"nicest", "foo"} {
    isprefix := trie.HasKeysWithPrefix(tofind)
    fmt.Printf("trie.HasKeysWithPrefix(\"%s\") = %v\n", tofind, isprefix)
    if isprefix {
      t.Errorf("trie.HasKeysWithPrefix(\"%s\") = true: expected false", tofind)
    }
  }
}
