import flet as ft

import psutil
from datetime import datetime

from apps.sms import SMSApp
from apps.calculator import CalculatorApp
from src.apps.inbox import InboxApp
from src.apps.snake import SnakeApp


class Fokia3310App:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self._init_state()
        self._build_ui()
        self.show_home()

    # page settingg
    def _setup_page(self):
        self.page.title = "Fokia 3310"
        self.page.bgcolor = "#0a0a0a"
        self.page.window.width = 300
        self.page.window.height = 650
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.padding = 10

    def _init_state(self):
        self.apps = {
            "SMS": SMSApp(self),
            "Calculator": CalculatorApp(self),
            "Inbox":InboxApp(self),
            "Game": SnakeApp(self),
        }
        self.current_app = None
        self.current_screen = "home"
        self.selected_menu_index = 0
        self.menu_options = ["SMS", "Calculator", "Inbox", "Game"]

        self.display_area = ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
        )

    def _build_ui(self):
        phone_body = ft.Container(
            content=ft.Column(
                controls=[
                    # Logo
                    ft.Container(
                        content=ft.Text(
                            "FOKIA",
                            color="#b8c5d6",
                            weight=ft.FontWeight.W_900,
                            size=16,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        padding=ft.padding.only(top=5, bottom=8),
                    ),

                    # Display screen
                    ft.Container(
                        content=self.display_area,
                        padding=12,
                        bgcolor="#a4b494",
                        border_radius=8,
                        border=ft.border.all(6, "#1a1a1a"),
                        height=160,
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=8,
                            color="#30000000",
                            offset=ft.Offset(0, 2),
                        ),
                    ),

                    # Nav controls
                    self._build_navigation_section(),

                    # Call buttons
                    self._build_action_section(),

                    # Numeric keypad
                    self._build_keypad_section(),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#34495e",
            padding=15,
            border_radius=30,
            expand=True,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=20,
                color="#60000000",
                offset=ft.Offset(0, 4),
            ),
        )

        self.page.add(phone_body)

    def _build_navigation_section(self):

        btn_color = "#2c3e50"

        return ft.Column(
            controls=[
                # Up arrow
                ft.Container(
                    content=ft.Icon(ft.Icons.KEYBOARD_ARROW_UP_ROUNDED, color=btn_color, size=22),
                    width=40,
                    height=35,
                    border_radius=8,
                    alignment=ft.Alignment(0, 0),
                    on_click=lambda _: self._handle_arrow("up"),
                    bgcolor="#95a5a6",
                ),
                # Left, OK, Right
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(ft.Icons.KEYBOARD_ARROW_LEFT_ROUNDED, color=btn_color, size=22),
                            width=40,
                            height=40,
                            border_radius=8,
                            alignment=ft.Alignment(0, 0),
                            on_click=lambda _: self._handle_arrow("left"),
                            bgcolor="#95a5a6",
                        ),
                        ft.Container(
                            content=ft.Text(
                                "OK",
                                weight=ft.FontWeight.BOLD,
                                size=13,
                                color="#2c3e50",
                            ),
                            bgcolor="#bdc3c7",
                            width=45,
                            height=45,
                            border_radius=23,
                            alignment=ft.Alignment(0, 0),
                            on_click=self._handle_ok,
                            shadow=ft.BoxShadow(
                                spread_radius=0,
                                blur_radius=4,
                                color="#40000000",
                                offset=ft.Offset(0, 2),
                            ),
                        ),
                        ft.Container(
                            content=ft.Icon(ft.Icons.KEYBOARD_ARROW_RIGHT_ROUNDED, color=btn_color, size=22),
                            width=40,
                            height=40,
                            border_radius=8,
                            on_click=lambda _: self._handle_arrow("right"),
                            alignment=ft.Alignment(0, 0),
                            bgcolor="#95a5a6",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                # Down arrow
                ft.Container(
                    content=ft.Icon(ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED, color=btn_color, size=22),
                    width=40,
                    height=35,
                    border_radius=8,
                    alignment=ft.Alignment(0, 0),
                    on_click=lambda _: self._handle_arrow("down"),
                    bgcolor="#95a5a6",
                ),
            ],
            spacing=3,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_action_section(self):
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(ft.Icons.CALL_ROUNDED, color="white", size=20),
                    bgcolor="#27ae60",
                    width=40,
                    height=40,
                    on_click=self._handle_call,
                    border_radius=20,
                    alignment=ft.Alignment(0, 0),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color="#40000000",
                        offset=ft.Offset(0, 2),
                    ),
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.CALL_END_ROUNDED, color="white", size=20),
                    bgcolor="#e74c3c",
                    width=40,
                    height=40,
                    border_radius=20,
                    alignment=ft.Alignment(0, 0),
                    on_click=self._handle_end,
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        color="#40000000",
                        offset=ft.Offset(0, 2),
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=40,
        )

    def _build_keypad_section(self):
        """Build the numeric keypad"""
        keys = [
            [("1", ".,"), ("2", "ABC"), ("3", "DEF")],
            [("4", "GHI"), ("5", "JKL"), ("6", "MNO")],
            [("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ")],
            [("*", "+"), ("0", " "), ("#", "⇧")],
        ]

        rows = []
        for row in keys:
            buttons = []
            for num, sub in row:
                buttons.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    num,
                                    weight=ft.FontWeight.BOLD,
                                    size=16,
                                    color="#2c3e50",
                                ),
                                ft.Text(
                                    sub,
                                    size=7,
                                    color="#7f8c8d",
                                ),
                            ],
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        width=55,
                        height=38,
                        bgcolor="#ecf0f1",
                        border_radius=6,
                        alignment=ft.Alignment(0, 0),
                        on_click=lambda e, k=num: self._handle_key(k),
                        shadow=ft.BoxShadow(
                            spread_radius=0,
                            blur_radius=3,
                            color="#30000000",
                            offset=ft.Offset(0, 1),
                        ),
                    )
                )
            rows.append(
                ft.Row(
                    controls=buttons,
                    spacing=8,
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        return ft.Column(
            controls=rows,
            spacing=6,
        )



    def show_home(self):

        self.current_screen = "home"
        self.current_app = None

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            status = "Plugged In" if plugged else "Discharging"
        else:
            percent = "N/A"
            status = "No battery detected"




        self.display_area.content = ft.Column(
            controls=[
                ft.Container(
                    ft.Text(
                        str(percent) + "% " + str(status),
                        size=10,
                        color="#2c3e50",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.RIGHT,
                    ),
                    align=ft.Alignment.TOP_RIGHT,
                ),
                ft.Text(
                    "FOKIA",
                    weight=ft.FontWeight.W_900,
                    size=24,
                    color="#2c3e50",
                ),
                # ft.Container(height=3),
                ft.Text(
                    current_time,
                    size=16,
                    color="#34495e",
                    weight=ft.FontWeight.W_500,
                ),
                ft.Text(
                    current_date,
                    size=12,
                    color="#34495e",
                    weight=ft.FontWeight.W_400,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.page.update()


    def show_menu(self):
        self.current_screen = "menu"
        self.current_app = None

        items = []
        for i, opt in enumerate(self.menu_options):
            selected = i == self.selected_menu_index
            items.append(
                ft.Container(
                    content=ft.Text(
                        f"{'▶ ' if selected else '  '}{opt}",
                        color="#2c3e50" if selected else "#4a5d6e",
                        weight=ft.FontWeight.BOLD if selected else ft.FontWeight.NORMAL,
                        size=12,
                    ),
                    bgcolor="#8a9b7a" if selected else None,
                    padding=3,
                    border_radius=4,
                )
            )

        self.display_area.content = ft.Column(
            controls=[
                ft.Text(
                    "Menu",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color="#2c3e50",
                    align=ft.Alignment.CENTER,
                ),
                ft.Container(height=0.5),
                ft.Column(
                    controls=items,
                    spacing=3,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START,
        )
        self.page.update()

    # def launch_app(self, name):
    #     self.current_app = self.apps.get(name)
    #     self.current_screen = "app"
    #
    #     if self.current_app:
    #         self.display_area.content = self.current_app.build()
    #     else:
    #         self.display_area.content = ft.Text(
    #             "App not found",
    #             color="#e74c3c",
    #             weight=ft.FontWeight.BOLD,
    #         )
    #
    #     self.page.update()

    def launch_app(self, name):
        self.current_app = self.apps.get(name)
        self.current_screen = "app"

        if self.current_app:
            self.display_area.content = self.current_app.build(
                width=160,
                height=136  # 160 - padding - header feeling
            )
        else:
            self.display_area.content = ft.Text("App not found")

        self.page.update()

    # ================= INPUT HANDLERS =================

    def _handle_ok(self, _):
        if self.current_screen == "home":
            self.show_menu()
        elif self.current_screen == "menu":
            self.launch_app(self.menu_options[self.selected_menu_index])

    def _handle_end(self, _):
        if self.current_screen == "app" and self.current_app:
            self.current_app.on_back()
        elif self.current_screen == "menu":
            self.show_home()

    def _handle_call(self, _):
        if self.current_screen == "app" and self.current_app:
            self.current_app.on_call()

    def _handle_arrow(self, direction):
        if self.current_screen == "menu":
            if direction == "up":
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_options)
            elif direction == "down":
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_options)
            self.show_menu()
        elif self.current_screen == "app" and self.current_app:
            self.current_app.on_arrow(direction)

    def _handle_key(self, key):
        if self.current_screen == "app" and self.current_app:
            self.current_app.on_key(key)


def main(page: ft.Page):
    Fokia3310App(page)


if __name__ == "__main__":
    ft.app(target=main)