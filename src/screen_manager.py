from screens.home_screen import HomeScreen
from screens.menu_screen import MenuScreen
from screens.calculator_screen import CalculatorScreen
from screens.snake_screen import SnakeScreen
from screens.sms_screen import SMSScreen
from screens.saper_screen import SaperScreen


class ScreenManager:
    """Manager zarządzający przełączaniem między ekranami"""

    def __init__(self, canvas, app):
        self.canvas = canvas
        self.app = app
        self.current_screen = None
        self.screen_history = []

        # Rejestracja dostępnych ekranów
        self.screens = {
            "home": HomeScreen,
            "menu": MenuScreen,
            "calculator": CalculatorScreen,
            "snake": SnakeScreen,
            "sms": SMSScreen,
            "saper": SaperScreen,
        }

    def show_screen(self, screen_name, **kwargs):
        """Pokazuje wybrany ekran"""
        # Zatrzymaj poprzedni ekran jeśli istnieje
        if self.current_screen:
            self.current_screen.stop()
            # Dodaj do historii (ale nie duplikuj)
            if not self.screen_history or self.screen_history[-1] != type(self.current_screen).__name__.lower().replace(
                    'screen', ''):
                self.screen_history.append(type(self.current_screen).__name__.lower().replace('screen', ''))

        # Utwórz nowy ekran
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name](self.canvas, self, **kwargs)
            self.current_screen.draw()
        else:
            print(f"Ekran '{screen_name}' nie istnieje!")

    def go_back(self):
        """Wraca do poprzedniego ekranu"""
        if len(self.screen_history) > 0:
            previous = self.screen_history.pop()
            self.show_screen(previous)
        else:
            self.show_screen("home")

    def handle_arrow(self, direction):
        """Przekazuje zdarzenie strzałki do aktualnego ekranu"""
        if self.current_screen:
            self.current_screen.handle_arrow(direction)

    def handle_center(self):
        """Przekazuje zdarzenie przycisku OK do aktualnego ekranu"""
        if self.current_screen:
            self.current_screen.handle_center()

    def handle_numpad(self, key):
        """Przekazuje zdarzenie klawiatury do aktualnego ekranu"""
        if self.current_screen:
            self.current_screen.handle_numpad(key)

    def handle_call(self):
        """Przekazuje zdarzenie przycisku Call do aktualnego ekranu"""
        if self.current_screen:
            self.current_screen.handle_call()

    def handle_end(self):
        """Obsługuje przycisk End - powrót lub wyjście"""
        if self.current_screen:
            # Najpierw daj ekranowi szansę obsłużyć end
            handled = self.current_screen.handle_end()
            if not handled:
                # Jeśli ekran nie obsłużył, cofnij się
                self.go_back()