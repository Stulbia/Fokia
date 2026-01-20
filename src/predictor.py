class T9TrieNode:
    def __init__(self):
        self.children = {}
        self.words = []  # Lista słów kończących się w tym punkcie lub przechodzących przez niego

class T9Predictor:
    def __init__(self, dictionary, char_to_digit):
        self.root = T9TrieNode()
        self.char_to_digit = char_to_digit
        self._build_trie(dictionary)

    def _build_trie(self, dictionary):
        for word in dictionary:
            seq = "".join(self.char_to_digit[c] for c in word)
            node = self.root
            # Dodajemy słowo do każdego węzła na ścieżce jego sekwencji
            for digit in seq:
                if digit not in node.children:
                    node.children[digit] = T9TrieNode()
                node = node.children[digit]
                node.words.append(word)

            # Sortujemy listy słów w węzłach zgodnie z Twoimi wymaganiami
            # (długość, potem alfabet)
            for digit in seq: # Opcjonalna optymalizacja: sortowanie po zbudowaniu całego drzewa
                pass

    def sort_all_nodes(self, node=None):
        """Sortuje listy słów w każdym węźle (wywoływane raz po zbudowaniu)"""
        if node is None: node = self.root
        node.words.sort(key=lambda w: (len(w), w))
        for child in node.children.values():
            self.sort_all_nodes(child)