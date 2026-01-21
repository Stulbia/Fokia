import flet as ft
from src.apps.base_app import BaseApp
from src.apps.t9_dictionary import T9Dictionary
from datetime import datetime


class SMSApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)
        self.text = ""
        self.current_sequence = ""
        self.current_abc_word = ""
        self.suggestions = []
        self.selected_suggestion = 0
        self.mode = "t9"  # "t9" or "abc" -> abc for adding new stuff
        self.last_key = None
        self.last_key_time = 0
        self.same_key_count = 0

        self.display = None
        self.suggestion_text = None
        self.message_text = None

#dict class
        self.dictionary = T9Dictionary()
        self.T9_MAP = T9Dictionary.T9_MAP

    def build(self, width, height):
        self.display = ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        ft.Text(
                            "SMS",
                            weight=ft.FontWeight.BOLD,
                            size=14,
                            color="#2c3e50",
                        ),
                        ft.Text(
                            f"[{self.mode.upper()}]",
                            size=10,
                            color="#7f8c8d",
                        ),
                    ],
                    spacing=5,
                ),
                ft.Container(height=4),

                # Magic
                ft.Container(
                    content=ft.Text(
                        "",
                        size=9,
                        color="#27ae60",
                        weight=ft.FontWeight.BOLD,
                    ),
                    height=15,
                ),

                # Message SMS
                ft.Container(
                    content=ft.Text(
                        self.text if self.text else "...",
                        size=11,
                        color="#2c3e50",
                    ),
                    height=60,
                ),
                ft.Container(height=5),

                # HELP
                ft.Text("0=spacja ↑↓=słowa", size=7, color="#000000"),
                ft.Text("#=tryb ##=zapis", size=7, color="#000000"),
                ft.Text("*=usuń CALL=zapis", size=7, color="#000000"),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )

        self.suggestion_text = self.display.controls[2].content
        self.message_text = self.display.controls[3].content

        return self.display

    def on_key(self, key):
        current_time = datetime.now().timestamp()

        # save or toggle
        if key == "#":
            if current_time - self.last_key_time < 0.5 and self.last_key == "#":
                self._save_message()
            else:
                self._toggle_mode()
            self.last_key = key
            self.last_key_time = current_time
            return

        # delete last (*)
        if key == "*":
            if self.mode == "t9" and self.current_sequence:
                self._cancel_word()
            elif self.text:
                self.text = self.text[:-1]
            self._update_display()
            return

        # Spacebar (0)
        if key == "0":
            # self._accept_word()
            if self.mode == "abc":
                self._add_current_word_to_dictionary()
            else:
                self._accept_word()
            self.text += " "
            self._update_display()
            return

        # T9  /  ABC
        if self.mode == "t9":
            self._handle_t9_key(key)
        else:
            self._handle_abc_key(key, current_time)

        self.last_key = key
        self.last_key_time = current_time

    def on_arrow(self, direction):
        """Obsługa strzałek do nawigacji po podpowiedziach"""
        if self.mode != "t9" or not self.suggestions:
            return

        if direction == "up":
            self.selected_suggestion = (self.selected_suggestion - 1) % len(self.suggestions)
        elif direction == "down":
            self.selected_suggestion = (self.selected_suggestion + 1) % len(self.suggestions)
        elif direction == "left":
            # Cofnij o jeden klawisz w sekwencji
            if self.current_sequence:
                self.current_sequence = self.current_sequence[:-1]
                self._update_suggestions()
        elif direction == "right":
            # Zaakceptuj słowo
            self._accept_word()

        self._update_display()

    def on_call(self):
        """Zapisz wiadomość klawiszem CALL"""
        self._save_message()

    def _handle_t9_key(self, key):
        if key in self.T9_MAP:
            self.current_sequence += key
            self._update_suggestions()
            self._update_display()

    # def _handle_abc_key(self, key, current_time):
    #     if key not in self.T9_MAP:
    #         return
    #
    #     chars = self.T9_MAP[key]
    #
    #     if key == self.last_key and current_time - self.last_key_time < 1.0:
    #         self.same_key_count = (self.same_key_count + 1) % len(chars)
    #         if self.text:
    #             self.text = self.text[:-1]
    #     else:
    #         self.same_key_count = 0
    #
    #     self.text += chars[self.same_key_count]
    #     self._update_display()

    def _handle_abc_key(self, key, current_time):
        if key not in self.T9_MAP:
            return

        chars = self.T9_MAP[key]

        if key == self.last_key and current_time - self.last_key_time < 1.0:
            self.same_key_count = (self.same_key_count + 1) % len(chars)
            if self.text:
                self.text = self.text[:-1]
                # Usuwamy też ostatnią literę z bufora ABC
                self.current_abc_word = self.current_abc_word[:-1]
        else:
            self.same_key_count = 0

        char = chars[self.same_key_count]
        self.text += char
        self.current_abc_word += char  # Zapamiętujemy wpisany znak
        self._update_display()

    def _update_suggestions(self):
        if not self.current_sequence:
            self.suggestions = []
            self.selected_suggestion = 0
            return

        self.suggestions = self.dictionary.get_suggestions(self.current_sequence, limit=5)
        self.selected_suggestion = 0

    def _accept_word(self):
        if self.mode == "t9" and self.suggestions:
            word = self.suggestions[self.selected_suggestion]
            self.text += word
            self.current_sequence = ""
            self.suggestions = []
            self.selected_suggestion = 0

    def _cancel_word(self):
        self.current_sequence = ""
        self.suggestions = []
        self.selected_suggestion = 0

    def _toggle_mode(self):
        self.mode = "abc" if self.mode == "t9" else "t9"
        self._cancel_word()
        self._update_display()

    def _update_display(self):
        if not self.display:
            return

        # update suggested
        if self.mode == "t9" and self.suggestions:
            suggestion_str = " ".join(
                f">{word}<" if i == self.selected_suggestion else word
                for i, word in enumerate(self.suggestions)
            )
            self.suggestion_text.value = suggestion_str
        else:
            self.suggestion_text.value = ""

        display_text = self.text
        if self.mode == "t9" and self.current_sequence:
            if self.suggestions:
                display_text += f"[{self.suggestions[self.selected_suggestion]}]"
            else:
                display_text += f"[{self.current_sequence}]"

        self.message_text.value = display_text if display_text else "..."

        # update mode
        self.display.controls[0].controls[1].value = f"[{self.mode.upper()}]"

        self.phone.page.update()

    def _save_message(self):
        if not self.text.strip():
            return

        # word ok in t9
        if self.mode == "t9" and self.suggestions:
            self._accept_word()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"sms_{timestamp}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Treść:\n{self.text}\n")

            # aight
            self.message_text.value = f"Sent!"
            self.text = ""
            self.current_sequence = ""
            self.suggestions = []
            self.phone.page.update()
        except Exception as e:
            self.message_text.value = f"ERROR: {str(e)}"
            self.phone.page.update()

    def on_back(self):
        self.phone.show_menu()

    def _add_current_word_to_dictionary(self):
        word_to_add = self.current_abc_word.strip()
        if len(word_to_add) > 1:  # Nie dodajemy pojedynczych liter
            # Wywołujemy metodę Twojej klasy T9Dictionary
            self.dictionary.add_word(word_to_add)
            # Opcjonalnie: wyświetl feedback użytkownikowi
            print(f"Dodano do słownika: {word_to_add}")

        self.current_abc_word = ""  # Czyścimy bufor po dodaniu