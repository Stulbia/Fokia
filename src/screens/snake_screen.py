from screens.base_screen import BaseScreen
import random


class SnakeScreen(BaseScreen):
    """Ekran gry Snake"""

    def __init__(self, canvas, screen_manager):
        super().__init__(canvas, screen_manager)
        self.grid_size = 8  # Rozmiar pojedynczej komórki
        self.grid_width = 20  # Ilość komórek w poziomie
        self.grid_height = 13  # Ilość komórek w pionie

        # Stan gry
        self.snake = [(10, 6), (9, 6), (8, 6)]  # Pozycje węża
        self.direction = (1, 0)  # Kierunek: (dx, dy)
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False

        # Timer gry
        self.game_loop()

    def spawn_food(self):
        """Generuje jedzenie w losowym miejscu"""
        while True:
            food = (random.randint(0, self.grid_width - 1),
                    random.randint(1, self.grid_height - 1))  # 1 zamiast 0 dla paska score
            if food not in self.snake:
                return food

    def draw(self):
        super().draw()

        if self.game_over:
            self.draw_game_over()
            return

        # Pasek z wynikiem
        self.draw_text(f"Score: {self.score}", 84, 8, font_size=8)

        # Rysowanie jedzenia
        fx, fy = self.food
        self.draw_rectangle(
            fx * self.grid_size,
            fy * self.grid_size + 4,
            (fx + 1) * self.grid_size,
            (fy + 1) * self.grid_size + 4,
            fill='#c0392b'
        )

        # Rysowanie węża
        for idx, (x, y) in enumerate(self.snake):
            color = '#2c3e50' if idx == 0 else '#34495e'  # Głowa ciemniejsza
            self.draw_rectangle(
                x * self.grid_size,
                y * self.grid_size + 4,
                (x + 1) * self.grid_size,
                (y + 1) * self.grid_size + 4,
                fill=color
            )

        if self.paused:
            self.draw_text("PAUZA", 84, 60, font_size=12)

    def draw_game_over(self):
        """Rysuje ekran końca gry"""
        self.draw_text("GAME OVER", 84, 40, font_size=12)
        self.draw_text(f"Wynik: {self.score}", 84, 60, font_size=10)
        self.draw_text("OK - restart", 84, 80, font_size=8)
        self.draw_text("End - wyjdź", 84, 95, font_size=8)

    def game_loop(self):
        """Główna pętla gry"""
        if not self.running or self.game_over or self.paused:
            return

        # Aktualizuj kierunek
        self.direction = self.next_direction

        # Oblicz nową pozycję głowy
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Sprawdź kolizje
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
                new_head[1] < 1 or new_head[1] >= self.grid_height or
                new_head in self.snake):
            self.game_over = True
            self.draw()
            return

        # Przesuń węża
        self.snake.insert(0, new_head)

        # Sprawdź czy zjadł jedzenie
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()  # Usuń ogon

        self.draw()

        # Następna klatka (szybkość gry)
        speed = max(100, 300 - self.score * 5)  # Przyspiesza z wynikiem
        self.canvas.after(speed, self.game_loop)

    def handle_arrow(self, direction):
        """Zmiana kierunku węża"""
        if self.game_over or self.paused:
            return

        directions = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        new_dir = directions.get(direction)
        if new_dir:
            # Nie pozwól zawrócić o 180 stopni
            if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
                self.next_direction = new_dir

    def handle_center(self):
        """OK - pauza lub restart"""
        if self.game_over:
            self.restart_game()
        else:
            self.paused = not self.paused
            self.draw()
            if not self.paused:
                self.game_loop()

    def restart_game(self):
        """Restart gry"""
        self.snake = [(10, 6), (9, 6), (8, 6)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.draw()
        self.game_loop()

    def stop(self):
        """Zatrzymaj grę"""
        super().stop()