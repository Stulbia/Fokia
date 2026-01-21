import json
import os
from collections import defaultdict

class T9Dictionary:
    T9_MAP = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    def __init__(self, dict_file="t9_dictionary.json", build_index=True):
        self.dict_file = dict_file
        self.trie = {}

        self.char_to_key = self._build_char_map()

        if os.path.exists(dict_file):
            self._load_words(dict_file)
        else:
            self.words = []
            if build_index:
                self._save_words()

    #  LOAD

    def _build_char_map(self):
        m = {}
        for key, chars in self.T9_MAP.items():
            for c in chars:
                m[c] = key
        return m

    def _load_words(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.words = json.load(f)

        self._build_trie()

    def _save_words(self):
        with open(self.dict_file, "w", encoding="utf-8") as f:
            json.dump(self.words, f, ensure_ascii=False)

    # TRIE (for easier search)
    def _insert_word(self, word):
        node = self.trie

        for ch in word:
            key = self.char_to_key.get(ch)
            if not key:
                continue
            node = node.setdefault(key, {})

        node.setdefault("_", []).append(word)

    def _build_trie(self):
        self.trie = {}

        for word in self.words:
            self._insert_word(word.lower())

        # Sort all word lists after building
        # sorting so shortest appear first
        # i do it here so i dont have to do it while searching
        self._sort_trie(self.trie)


    def _sort_trie(self, node):
        if "_" in node:
            node["_"].sort(key=lambda w: (len(w), w))

        # something smart that I probably need to remember but won't anyways
        for key, child in node.items():
            if key != "_":
                self._sort_trie(child)

    # +++++++++++++++++++++++++++++API = INTERFACE
    def get_suggestions(self, sequence, limit=5):
        node = self.trie

        for digit in sequence:
            node = node.get(digit)
            if not node:
                return []

        results = []
        self._collect_words(node, results)
        return results[:limit]

    def _collect_words(self, node, results):
        if "_" in node:
            results.extend(node["_"])

        for key, child in node.items():
            if key != "_":
                self._collect_words(child, results)

    def add_word(self, word):
        word = word.lower()
        if word in self.words:
            return

        self.words.append(word)
        self._insert_word(word)
        self._save_words()
