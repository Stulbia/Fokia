from screens.base_screen import BaseScreen

# --- STRUKTURA TRIE DLA T9 ---

class T9TrieNode:
    def __init__(self):
        self.children = {}
        self.words = []  # Przechowuje słowa pasujące do tego prefiksu


class T9Predictor:
    def __init__(self, dictionary, char_to_digit):
        self.root = T9TrieNode()
        self.char_to_digit = char_to_digit
        self._build_trie(dictionary)

    def _build_trie(self, dictionary):
        for word in dictionary:
            # Zamień słowo na cyfry, np. "home" -> "4663"
            seq = "".join(self.char_to_digit.get(c, '') for c in word.lower())
            node = self.root
            # Wstawiamy słowo do każdego węzła na jego ścieżce (dla wyszukiwania prefiksowego)
            for digit in seq:
                if digit not in node.children:
                    node.children[digit] = T9TrieNode()
                node = node.children[digit]
                node.words.append(word)

        # Sortujemy słowa w każdym węźle: najpierw długość, potem alfabet
        self._sort_node_words(self.root)

    def _sort_node_words(self, node):
        node.words.sort(key=lambda w: (len(w), w))
        for child in node.children.values():
            self._sort_node_words(child)

    def get_suggestions(self, sequence):
        node = self.root
        for digit in sequence:
            if digit in node.children:
                node = node.children[digit]
            else:
                return []
        return node.words


# --- GŁÓWNA KLASA EKRANU ---

class SMSScreen(BaseScreen):
    MAX_LEN = 160

    def __init__(self, canvas, screen_manager):
        super().__init__(canvas, screen_manager)

        self.text = ""
        self.input_mode = "PREDICT"  # PREDICT | T9
        self.shift = False

        self.t9_map = {
            '2': 'abc', '3': 'def', '4': 'ghi',
            '5': 'jkl', '6': 'mno', '7': 'pqrs',
            '8': 'tuv', '9': 'wxyz', '0': ' '
        }

        self.char_to_digit = {c: k for k, v in self.t9_map.items() for c in v}

        self.dictionary = [
            "hello", "hip", "his", "home", "good", "bad", "yes", "no",
            "thanks", "thank", "you", "ok", "cool", "test",
            "sms", "message", "love", "call", "me", "later", "go", "ice"
        ]

        # Inicjalizacja Trie
        self.trie = T9Predictor(self.dictionary, self.char_to_digit)

        self.sequence = ""
        self.suggestions = []
        self.suggestion_index = 0

        self.last_key = None
        self.key_press_count = 0
        self.key_timer = None

    # ================= LOGIKA T9 PREDICTIVE =================

    def handle_predictive_t9(self, key):
        if key == '0':
            self.commit_word(space=True)
            return

        if key not in self.t9_map:
            return

        self.sequence += key
        # Pobieramy sugestie z Trie (już posortowane przy budowie)
        self.suggestions = self.trie.get_suggestions(self.sequence)
        self.suggestion_index = 0
        self.draw()

    def commit_word(self, space=False):
        if not self.sequence:
            if space:
                self.text += " "
                self.draw()
            return

        # Jeśli brak słowa w słowniku, wpisz cyfry
        word = self.suggestions[self.suggestion_index] if self.suggestions else self.sequence

        if self.shift:
            word = word.upper()

        self.text += word
        if space:
            self.text += " "

        self.sequence = ""
        self.suggestions = []
        self.suggestion_index = 0
        self.draw()

    # ================= POZOSTAŁE METODY =================

    def draw(self):
        super().draw()
        mode = {"PREDICT": "T9+", "T9": "T9"}[self.input_mode]
        shift = "A" if self.shift else "a"

        self.draw_text(f"SMS [{mode} {shift}]", 84, 12, font_size=8)
        self.canvas.create_line(10, 22, 158, 22, fill="#1a1a1a")

        # Podgląd tekstu + aktualnie wpisywane słowo
        preview = self.preview_word()
        full_text_view = self.text + preview
        lines = self.wrap_text(full_text_view, 20)

        y = 35
        for l in lines[:4]:
            self.draw_text(l, 10, y, font_size=8, anchor="w")
            y += 15

        self.draw_text(f"{len(self.text)}/{self.MAX_LEN}", 84, 110, font_size=7)

        # Wyświetlanie paska sugestii
        if self.input_mode == "PREDICT" and self.suggestions:
            current = self.suggestions[self.suggestion_index]
            self.draw_text(f"[{current}]", 84, 98, font_size=7)

        self.draw_text("* tryb | # shift | 0 spacja", 84, 118, font_size=6)

    def preview_word(self):
        if self.input_mode != "PREDICT" or not self.sequence:
            return ""
        return self.suggestions[self.suggestion_index] if self.suggestions else self.sequence

    def wrap_text(self, text, width):
        if not text: return [""]
        words = text.split(" ")
        lines, cur = [], ""
        for w in words:
            if len(cur + w) <= width:
                cur += w + " "
            else:
                lines.append(cur.rstrip())
                cur = w + " "
        if cur:
            lines.append(cur.rstrip())
        return lines

    def handle_numpad(self, key):
        if len(self.text) >= self.MAX_LEN: return

        if key == '*':
            self.switch_mode()
            return
        if key == '#':
            self.shift = not self.shift
            self.draw()
            return

        if self.input_mode == "T9":
            self.handle_classic_t9(key)
        else:
            self.handle_predictive_t9(key)

    def handle_arrow(self, direction):
        if self.input_mode == "PREDICT" and self.suggestions:
            if direction == "up":
                self.suggestion_index = (self.suggestion_index - 1) % len(self.suggestions)
            elif direction == "down":
                self.suggestion_index = (self.suggestion_index + 1) % len(self.suggestions)
            self.draw()

    def handle_call(self):
        if self.input_mode == "PREDICT":
            self.commit_word()
        else:
            self.text = ""
            self.draw()

    def switch_mode(self):
        self.confirm_letter()
        self.sequence = ""
        self.suggestions = []
        self.input_mode = "T9" if self.input_mode == "PREDICT" else "PREDICT"
        self.draw()

    def handle_classic_t9(self, key):
        if key not in self.t9_map: return
        chars = self.t9_map[key]
        if self.key_timer: self.canvas.after_cancel(self.key_timer)

        if key == self.last_key:
            self.key_press_count = (self.key_press_count + 1) % len(chars)
            self.text = self.text[:-1]
        else:
            self.key_press_count = 0
            self.last_key = key

        ch = chars[self.key_press_count]
        if self.shift: ch = ch.upper()
        self.text += ch
        self.draw()
        self.key_timer = self.canvas.after(1000, self.confirm_letter)

    def confirm_letter(self):
        self.last_key = None
        self.key_press_count = 0

    def stop(self):
        if self.key_timer: self.canvas.after_cancel(self.key_timer)
        super().stop()