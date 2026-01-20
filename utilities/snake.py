import tkinter as tk
import random

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
WINDOW_WIDTH = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT = CELL_SIZE * GRID_HEIGHT + 40

BG_COLOR = '#c7f0d8'
SNAKE_COLOR = '#43523d'
FOOD_COLOR = '#43523d'
GRID_COLOR = '#a0c8b0'

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Snake - Nokia 3310 Style')
        self.root.resizable(False, False)

        # Canvas do rysowania
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        # Inicjalizacja gry
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.game_started = False

        # Sterowanie
        self.root.bind('<Up>', lambda e: self.change_direction(UP))
        self.root.bind('<Down>', lambda e: self.change_direction(DOWN))
        self.root.bind('<Left>', lambda e: self.change_direction(LEFT))
        self.root.bind('<Right>', lambda e: self.change_direction(RIGHT))
        self.root.bind('<space>', lambda e: self.restart_game())

        self.draw_start_screen()

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def change_direction(self, new_direction):
        if not self.game_started:
            self.game_started = True
            self.game_loop()

        # Nie pozwól na zawrócenie o 180 stopni
        if (self.direction[0] * -1, self.direction[1] * -1) != new_direction:
            self.direction = new_direction

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x, head_y + dir_y)

        # Sprawdź kolizję ze ścianami
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        # Sprawdź kolizję z własnym ciałem
        if new_head in self.snake:
            return False

        self.snake.insert(0, new_head)

        # Sprawdź czy zjedliśmy jedzenie
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

        return True

    def draw(self):
        self.canvas.delete('all')

        # Rysuj siatkę
        for i in range(GRID_WIDTH + 1):
            x = i * CELL_SIZE
            self.canvas.create_line(x, 40, x, WINDOW_HEIGHT, fill=GRID_COLOR, width=1)
        for i in range(GRID_HEIGHT + 1):
            y = i * CELL_SIZE + 40
            self.canvas.create_line(0, y, WINDOW_WIDTH, y, fill=GRID_COLOR, width=1)

        # Rysuj węża
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x * CELL_SIZE + 1, y * CELL_SIZE + 40 + 1,
                (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE + 40 - 1,
                fill=SNAKE_COLOR, outline=SNAKE_COLOR
            )

        # Rysuj jedzenie
        x, y = self.food
        self.canvas.create_rectangle(
            x * CELL_SIZE + 1, y * CELL_SIZE + 40 + 1,
            (x + 1) * CELL_SIZE - 1, (y + 1) * CELL_SIZE + 40 - 1,
            fill=FOOD_COLOR, outline=FOOD_COLOR
        )

        # Wyświetl wynik
        self.canvas.create_text(
            10, 20, text=f'Wynik: {self.score}',
            font=('Arial', 16, 'bold'), fill=SNAKE_COLOR, anchor='w'
        )

    def draw_start_screen(self):
        self.canvas.delete('all')
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40,
            text='SNAKE', font=('Arial', 32, 'bold'), fill=SNAKE_COLOR
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20,
            text='Użyj strzałek aby rozpocząć', font=('Arial', 12), fill=SNAKE_COLOR
        )

    def draw_game_over(self):
        self.canvas.create_rectangle(
            WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 - 60,
            WINDOW_WIDTH // 2 + 120, WINDOW_HEIGHT // 2 + 60,
            fill=BG_COLOR, outline=SNAKE_COLOR, width=2
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30,
            text='GAME OVER', font=('Arial', 20, 'bold'), fill=SNAKE_COLOR
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
            text=f'Wynik: {self.score}', font=('Arial', 16), fill=SNAKE_COLOR
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30,
            text='Naciśnij SPACJĘ', font=('Arial', 12), fill=SNAKE_COLOR
        )

    def game_loop(self):
        if not self.game_over and self.game_started:
            if self.move_snake():
                self.draw()
                self.root.after(100, self.game_loop)
            else:
                self.game_over = True
                self.draw()
                self.draw_game_over()

    def restart_game(self):
        if self.game_over:
            self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
            self.direction = RIGHT
            self.food = self.generate_food()
            self.score = 0
            self.game_over = False
            self.game_started = True
            self.game_loop()


if __name__ == '__main__':
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()