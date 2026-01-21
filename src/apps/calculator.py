import flet as ft
from apps.base_app import BaseApp


class CalculatorApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)
        self.expr = ""
        self.result = ""
        self.display = None

    def build(self):
        self.display = ft.Container(
            alignment=ft.alignment.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "CALCULATOR",
                        weight=ft.FontWeight.BOLD,
                        size=14,
                        color="#2c3e50",
                    ),
                    ft.Container(height=8),
                    ft.Text(
                        self.expr if self.expr else "0",
                        size=16,
                        color="#2c3e50",
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(
                        content=ft.Text(
                            self.result,
                            size=12,
                            color="#7f8c8d",
                            italic=True,
                        ),
                        height=20,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "CALL = result | * = clear",
                        size=8,
                        color="black",
                    ),
                    ft.Text(
                        "↑(+) ↓(-) ←(/) →(*)",
                        size=10,
                        weight=ft.FontWeight.BOLD,
                        color="#34495e",
                    ),
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
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
        # Map arrows to math operators
        mapping = {
            "up": "+",
            "down": "-",
            "left": "/",
            "right": "*"
        }

        if arrow in mapping:
            # Prevent starting with an operator or doubling them
            if self.expr and self.expr[-1] not in "+-*/":
                self.expr += mapping[arrow]
                self.result = ""
                self._update_display()

    def on_call(self):
        if self.expr:
            try:
                # Use a safe evaluation context if needed, here keeping it simple
                result = eval(self.expr)
                if isinstance(result, float):
                    result_str = f"{result:.6f}".rstrip('0').rstrip('.')
                else:
                    result_str = str(result)

                self.result = f"= {result_str}"
                self.expr = result_str
            except Exception:
                self.result = "ERROR"

        self._update_display()

    def _update_display(self):
        if self.display:
            # Column is inside the Container
            column = self.display.content
            column.controls[2].value = self.expr if self.expr else "0"
            column.controls[3].content.value = self.result
            self.phone.page.update()

    def on_back(self):
        self.phone.show_menu()