import flet as ft
from src.apps.base_app import BaseApp

#simple calculator because I want some filler apps and it's easy to make

class CalculatorApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)
        self.expr = ""
        self.result = ""
        self.display = None

    def build(self, width, height):
        # Wyliczamy wysokości
        header_height = 25
        expr_height = 30
        result_height = 20
        footer_height = 30
        spacing_total = 20

        self.display = ft.Container(
            width=width,
            height=height,
            content=ft.Column(
                controls=[
                    # Header
                    ft.Container(
                        content=ft.Text(
                            "KALKULATOR",
                            weight=ft.FontWeight.BOLD,
                            size=12,
                            color="#2c3e50",
                        ),
                        height=header_height,
                    ),

                    # Expression display
                    ft.Container(
                        content=ft.Text(
                            self.expr if self.expr else "0",
                            size=14,
                            color="#2c3e50",
                            weight=ft.FontWeight.W_500,
                        ),
                        height=expr_height,
                        alignment=ft.Alignment.CENTER,
                    ),

                    # Result display
                    ft.Container(
                        content=ft.Text(
                            self.result,
                            size=11,
                            color="#7f8c8d",
                            italic=True,
                        ),
                        height=result_height,
                        alignment=ft.Alignment.CENTER,
                    ),

                    # Footer instructions
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "↑(+) ↓(-) ←(/) →(*)",
                                    size=8,
                                    color="#7f8c8d",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    "CALL=solution; #=delete; *=clear",
                                    size=8,
                                    color="#7f8c8d",
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                            spacing=2,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        height=footer_height,
                    ),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        return self.display

    def on_key(self, key):
        if key in "0123456789":
            self.expr += key
            self.result = ""

        elif key == "*":
            self.expr = ""
            self.result = ""

        elif key == "#":
            if self.expr:
                self.expr = self.expr[:-1]
                self.result = ""

        self._update_display()

    def on_arrow(self, arrow):
        mapping = {
            "up": "+",
            "down": "-",
            "left": "/",
            "right": "*"
        }

        if arrow in mapping:
            if self.expr and self.expr[-1] not in "+-*/":
                self.expr += mapping[arrow]
                self.result = ""
                self._update_display()

    def on_call(self):
        if self.expr:
            try:
                result = eval(self.expr)
                if isinstance(result, float):
                    result_str = f"{result:.6f}".rstrip('0').rstrip('.')
                else:
                    result_str = str(result)

                self.result = f"= {result_str}"
                self.expr = result_str
            except Exception:
                self.result = "BŁĄD"

        self._update_display()

    def _update_display(self):
        if self.display:
            column = self.display.content
            column.controls[1].content.value = self.expr if self.expr else "0"
            column.controls[2].content.value = self.result
            self.phone.page.update()

    def on_back(self):
        self.phone.show_menu()