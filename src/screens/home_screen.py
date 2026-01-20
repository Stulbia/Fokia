from screens.base_screen import BaseScreen
from datetime import datetime


class HomeScreen(BaseScreen):
    """Ekran główny (home screen) telefonu"""

    def draw(self):
        super().draw()

        # Aktualna godzina
        current_time = datetime.now().strftime("%H:%M")
        self.draw_text(current_time, 84, 20, font_size=16)

        # Data
        current_date = datetime.now().strftime("%d-%m-%Y")
        self.draw_text(current_date, 84, 40, font_size=8)

        # Ikona sieci
        self.draw_text("📶", 150, 10, font_size=10)

        # Poziom baterii
        self.draw_text("🔋", 20, 10, font_size=10)

        # Logo/nazwa
        self.draw_text("FOKIA", 84, 70, font_size=14)

        # Instrukcja
        self.draw_text("Menu", 84, 100, font_size=8)
        self.draw_text("↓", 84, 110, font_size=8)

    def handle_center(self):
        """OK otwiera menu"""
        self.screen_manager.show_screen("menu")

    def handle_arrow(self, direction):
        """Strzałka w dół też otwiera menu"""
        if direction == "down":
            self.screen_manager.show_screen("menu")