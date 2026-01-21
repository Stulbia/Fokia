import flet as ft
import os
from apps.base_app import BaseApp


class InboxApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)
        self.messages = []  # Lista treści wiadomości
        self.current_index = 0  # Indeks aktualnie wyświetlanej wiadomości
        self.display = None
        self.content_text = None
        self.header_text = None

    def build(self):
        # Wczytujemy wiadomości przy starcie aplikacji
        self.messages = self._load_messages()

        # UI
        self.display = ft.Column(
            controls=[
                # Header
                ft.Row(
                    controls=[
                        ft.Text("SKRZYNKA", weight=ft.FontWeight.BOLD, size=14, color="#2c3e50"),
                        ft.Text(f"0/0", size=10, color="#7f8c8d"),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(height=10),

                # Miejsce na treść
                ft.Container(
                    content=ft.Text(
                        "Brak wiadomości" if not self.messages else "",
                        size=12,
                        color="#2c3e50",
                    ),
                    height=100,
                    padding=5,
                    border=ft.border.all(1, "#bdc3c7"),
                    border_radius=5,
                ),
                ft.Container(height=10),

                # Instrukcja
                ft.Text("← → wybierz  * usuń", size=8, color="#7f8c8d"),
            ],
            spacing=2,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Zgodnie z Twoim ustawieniem
        )

        self.header_text = self.display.controls[0].controls[1]
        self.content_text = self.display.controls[2].content

        self._update_ui()
        return self.display

    def _load_messages(self):
        """Wczytuje wszystkie pliki sms_*.txt z folderu"""
        msgs = []
        try:
            # Szukamy plików w bieżącym katalogu
            files = [f for f in os.listdir(".") if f.startswith("sms_") and f.endswith(".txt")]
            # Sortujemy od najnowszych (po nazwie pliku, bo zawiera datę)
            files.sort(reverse=True)

            for file in files:
                with open(file, "r", encoding="utf-8") as f:
                    msgs.append({"filename": file, "content": f.read()})
        except Exception as e:
            print(f"Błąd wczytywania: {e}")
        return msgs

    def on_key(self, key):
        if key == "*":  # Usuwanie wiadomości
            self._delete_current_message()

    def on_arrow(self, direction):
        if not self.messages:
            return

        if direction == "left":
            self.current_index = (self.current_index - 1) % len(self.messages)
        elif direction == "right":
            self.current_index = (self.current_index + 1) % len(self.messages)

        self._update_ui()

    def _delete_current_message(self):
        if not self.messages:
            return

        msg = self.messages[self.current_index]
        try:
            os.remove(msg["filename"])
            self.messages.pop(self.current_index)
            # Korekta indeksu po usunięciu
            if self.current_index >= len(self.messages) and self.messages:
                self.current_index = len(self.messages) - 1
            self._update_ui()
        except Exception as e:
            self.content_text.value = f"Błąd usuwania: {e}"
            self.phone.page.update()

    def _update_ui(self):
        if not self.messages:
            self.header_text.value = "0/0"
            self.content_text.value = "Skrzynka pusta"
        else:
            self.header_text.value = f"{self.current_index + 1}/{len(self.messages)}"
            self.content_text.value = self.messages[self.current_index]["content"]

        if self.phone:
            self.phone.page.update()

    def on_back(self):
        self.phone.show_menu()