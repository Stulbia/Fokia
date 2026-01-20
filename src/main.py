import flet as ft


class Nokia3310App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Fokia 3310 - Organized Layout"
        self.page.bgcolor = "#1a1a1a"
        self.page.window_width = 400
        self.page.window_height = 850

        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Stan aplikacji
        self.current_screen = "home"
        self.selected_menu_index = 0
        self.menu_options = ["Snake", "Saper", "SMS", "Calculator"]

        self.display_area = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
        )

        self.build_ui()
        self.show_home()

    def build_ui(self):
        self.phone_body = ft.Container(
            content=ft.Column([
                # 1. LOGO
                ft.Text("FOKIA", color="#ECF0F1", weight="bold", size=20),

                # 2. EKRAN (LCD)
                ft.Container(
                    content=self.display_area,
                    padding=10,
                    bgcolor="#9db88a",
                    border_radius=10,
                    border=ft.border.all(8, "#1A1A1A"),
                    expand=5,
                ),

                # 3. KONTENER NAWIGACJI (D-PAD)
                ft.Container(
                    content=self.build_navigation_section(),
                    expand=3,
                    alignment=ft.Alignment.CENTER,
                ),

                # 4. KONTENER POŁĄCZ/ROZŁĄCZ
                ft.Container(
                    content=self.build_action_section(),
                    expand=1,
                    alignment=ft.Alignment.CENTER,
                ),

                # 5. KONTENER KLAWIATURY NUMERYCZNEJ
                ft.Container(
                    content=self.build_keypad_section(),
                    expand=5,
                    alignment=ft.Alignment.CENTER,
                ),

            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            bgcolor="#2C3E50",
            padding=20,
            border_radius=40,
            expand=True,
            shadow=ft.BoxShadow(blur_radius=50, color="black"),
            margin=10
        )
        self.page.add(self.phone_body)

    def build_navigation_section(self):
        """Kontener na przyciski nawigacji (D-Pad)"""
        return ft.Column([
            ft.IconButton(ft.Icons.KEYBOARD_ARROW_UP, icon_size=30, on_click=lambda _: self.handle_arrow("up")),
            ft.Row([
                ft.IconButton(ft.Icons.KEYBOARD_ARROW_LEFT, icon_size=30),
                ft.Container(
                    content=ft.Text("OK", color="black", weight="bold"),
                    bgcolor="#BDC3C7", width=55, height=55, shape=ft.BoxShape.CIRCLE,
                    alignment=ft.Alignment.CENTER,
                    on_click=self.handle_ok
                ),
                ft.IconButton(ft.Icons.KEYBOARD_ARROW_RIGHT, icon_size=30),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            ft.IconButton(ft.Icons.KEYBOARD_ARROW_DOWN, icon_size=30, on_click=lambda _: self.handle_arrow("down")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=-10)

    def build_action_section(self):
        """Kontener na przyciski Połącz (Zielony) / Rozłącz (Czerwony)"""
        return ft.Row([
            ft.IconButton(
                icon=ft.Icons.CALL,
                icon_color="green",
                icon_size=35,
                tooltip="Call"
            ),
            ft.IconButton(
                icon=ft.Icons.CALL_END,
                icon_color="red",
                icon_size=35,
                on_click=self.handle_end,
                tooltip="End/Back"
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=60)

    def build_keypad_section(self):
        """Kontener na klawiaturę numeryczną"""
        keys = [
            [("1", ".,"), ("2", "ABC"), ("3", "DEF")],
            [("4", "GHI"), ("5", "JKL"), ("6", "MNO")],
            [("7", "PQRS"), ("8", "TUV"), ("9", "WXYZ")],
            [("*", "+"), ("0", "_"), ("#", "⇧")]
        ]
        rows = []
        for row_keys in keys:
            buttons = []
            for num, sub in row_keys:
                buttons.append(
                    ft.Container(
                        content=ft.ElevatedButton(
                            content=ft.Column([
                                ft.Text(num, size=16, weight="bold", color="black"),
                                ft.Text(sub, size=7, color="black")
                            ], spacing=0, alignment=ft.MainAxisAlignment.CENTER),
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8), padding=0),
                        ),
                        expand=True,
                    )
                )
            rows.append(ft.Row(controls=buttons, expand=True, spacing=8))
        return ft.Column(controls=rows, expand=True, spacing=8)

    # --- LOGIKA SYSTEMOWA (bez zmian) ---

    def show_home(self):
        self.current_screen = "home"
        self.display_area.content = ft.Column([
            ft.Icon(ft.Icons.SIGNAL_CELLULAR_4_BAR, color="black", size=20),
            ft.Text("NOKIA", color="black", weight="bold", size=30),
            ft.Text("12:00", color="black", size=15),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page.update()

    def show_menu(self):
        self.current_screen = "menu"
        menu_items = []
        for i, option in enumerate(self.menu_options):
            is_selected = i == self.selected_menu_index
            menu_items.append(
                ft.Container(
                    content=ft.Text(option.upper(), color="white" if is_selected else "black",
                                    weight="bold" if is_selected else "normal", size=18),
                    bgcolor="black" if is_selected else None,
                    padding=5, width=200, alignment=ft.Alignment.CENTER, border_radius=5
                )
            )
        self.display_area.content = ft.Column(controls=menu_items, alignment=ft.MainAxisAlignment.CENTER,
                                              horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page.update()

    def handle_ok(self, _):
        if self.current_screen == "home":
            self.show_menu()
        elif self.current_screen == "menu":
            self.launch_app(self.menu_options[self.selected_menu_index])

    def handle_end(self, _):
        if self.current_screen == "app":
            self.show_menu()
        elif self.current_screen == "menu":
            self.show_home()

    def handle_arrow(self, direction):
        if self.current_screen == "menu":
            if direction == "up":
                self.selected_menu_index = (self.selected_menu_index - 1) % len(self.menu_options)
            elif direction == "down":
                self.selected_menu_index = (self.selected_menu_index + 1) % len(self.menu_options)
            self.show_menu()

    def launch_app(self, name):
        self.current_screen = "app"
        self.display_area.content = ft.Column([
            ft.Text(name.upper(), color="black", weight="bold", size=25),
            ft.Text("App running...", color="black"),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page.update()


if __name__ == "__main__":
    ft.app(target=Nokia3310App)