import flet as ft
import os
from src.apps.base_app import BaseApp


class InboxApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)
        self.messages = []
        self.current_index = 0
        self.display = None
        self.content_text = None
        self.header_text = None

    def build(self, width, height):
        self.messages = self._load_messages()

        header_height = 30
        footer_height = 20
        spacing_total = 20
        content_height = height - header_height - footer_height - spacing_total

        self.display = ft.Container(
            width=width,
            height=height,
            content=ft.Column(
                controls=[
                    # Header
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text("INBOX", weight=ft.FontWeight.BOLD, size=12, color="#2c3e50"),
                                ft.Text(f"0/0", size=10, color="#7f8c8d"),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        height=header_height,
                    ),

                    # Content area /w height
                    ft.Container(
                        content=ft.Text(
                            "No messages." if not self.messages else "",
                            size=10,
                            color="#2c3e50",
                        ),
                        height=content_height,
                        width=width - 10,  # minus padding
                        padding=5,
                        border=ft.border.all(1, "#2c3e50"),
                        border_radius=5,
                        alignment=ft.Alignment.TOP_LEFT,
                    ),

                    # Footer
                    ft.Container(
                        content=ft.Text("← → choose  * delete", size=8, color="#2c3e50"),
                        height=footer_height,
                    ),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        self.header_text = self.display.content.controls[0].content.controls[1]
        self.content_text = self.display.content.controls[1].content

        self._update_ui()
        return self.display

    def _load_messages(self):
        msgs = []
        try:
            files = [f for f in os.listdir(".") if f.startswith("sms_") and f.endswith(".txt")]
            files.sort(reverse=True)

            for file in files:
                with open(file, "r", encoding="utf-8") as f:
                    msgs.append({"filename": file, "content": f.read()})
        except Exception as e:
            print(f"load error: {e}")
        return msgs

    def on_key(self, key):
        if key == "*":
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
            if self.current_index >= len(self.messages) and self.messages:
                self.current_index = len(self.messages) - 1
            self._update_ui()
        except Exception as e:
            self.content_text.value = f"delete error: {e}"
            self.phone.page.update()

    def _update_ui(self):
        if not self.messages:
            self.header_text.value = "0/0"
            self.content_text.value = "INBOX IS EMPTY."
        else:
            self.header_text.value = f"{self.current_index + 1}/{len(self.messages)}"
            self.content_text.value = self.messages[self.current_index]["content"]

        if self.phone:
            self.phone.page.update()

    def on_back(self):
        self.phone.show_menu()