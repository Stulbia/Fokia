from screens.base_screen import BaseScreen


class MenuScreen(BaseScreen):
    """Ekran menu głównego"""

    def __init__(self, canvas, screen_manager):
        super().__init__(canvas, screen_manager)
        self.menu_items = [
            ("SMS", "sms", "📨"),
            ("Snake", "snake", "🎮"),
            ("Kalkulator", "calculator", "🔢"),
            ("Saper", "saper", "💣"),
        ]
        self.selected_index = 0

    def draw(self):
        super().draw()

        # Tytuł
        self.draw_text("MENU", 84, 15, font_size=12)

        # Linia pod tytułem
        self.canvas.create_line(10, 25, 158, 25, fill='#1a1a1a', width=1)

        # Pozycje menu
        y_start = 40
        y_spacing = 20

        for idx, (name, screen, icon) in enumerate(self.menu_items):
            y = y_start + idx * y_spacing

            # Highlight dla wybranego
            if idx == self.selected_index:
                self.draw_rectangle(5, y - 8, 163, y + 10, fill='#7f8c8d')
                text_fill = 'white'
            else:
                text_fill = '#1a1a1a'

            # Ikona i tekst
            self.canvas.create_text(20, y, text=icon,
                                    font=('Arial', 10),
                                    fill=text_fill, anchor="w")
            self.canvas.create_text(45, y, text=name,
                                    font=('Arial', 10),
                                    fill=text_fill, anchor="w")

    def handle_arrow(self, direction):
        """Nawigacja po menu"""
        if direction == "up":
            self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            self.draw()
        elif direction == "down":
            self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            self.draw()

    def handle_center(self):
        """OK - wybiera pozycję menu"""
        _, screen_name, _ = self.menu_items[self.selected_index]
        self.screen_manager.show_screen(screen_name)

    def handle_end(self):
        """End - powrót do home"""
        self.screen_manager.show_screen("home")
        return True