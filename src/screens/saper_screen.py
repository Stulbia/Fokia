from screens.base_screen import BaseScreen
import random


class SaperScreen(BaseScreen):

    GRID_W = 8
    GRID_H = 8
    MINES = 10
    CELL = 18

    def __init__(self, canvas, screen_manager):
        super().__init__(canvas, screen_manager)
        self.cursor_x = 0
        self.cursor_y = 0
        self.init_board()

    # ================= INIT =================

    def init_board(self):
        self.board = [[0]*self.GRID_W for _ in range(self.GRID_H)]
        self.revealed = [[False]*self.GRID_W for _ in range(self.GRID_H)]
        self.flags = [[False]*self.GRID_W for _ in range(self.GRID_H)]

        self.mines_left = self.MINES
        self.game_over = False
        self.win = False

        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        placed = 0
        while placed < self.MINES:
            x = random.randint(0, self.GRID_W - 1)
            y = random.randint(0, self.GRID_H - 1)
            if self.board[y][x] != -1:
                self.board[y][x] = -1
                placed += 1

    def calculate_numbers(self):
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                if self.board[y][x] == -1:
                    continue
                self.board[y][x] = sum(
                    1 for dy in (-1, 0, 1) for dx in (-1, 0, 1)
                    if 0 <= x+dx < self.GRID_W and 0 <= y+dy < self.GRID_H
                    and self.board[y+dy][x+dx] == -1
                )

    # ================= DRAW =================

    def draw(self):
        super().draw()

        self.draw_text("SAPER", 84, 12, font_size=12)
        self.draw_text(f"Miny: {self.mines_left}", 84, 22, font_size=8)

        ox, oy = 10, 30

        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                px = ox + x * self.CELL
                py = oy + y * self.CELL

                if x == self.cursor_x and y == self.cursor_y:
                    self.draw_rectangle(px-2, py-2, px+self.CELL+2, py+self.CELL+2, fill="#3498db")

                if self.revealed[y][x]:
                    self.draw_rectangle(px, py, px+self.CELL, py+self.CELL, fill="#ecf0f1")
                    v = self.board[y][x]
                    if v == -1:
                        self.canvas.create_text(px+9, py+9, text="💣")
                    elif v > 0:
                        self.canvas.create_text(px+9, py+9, text=str(v))
                else:
                    self.draw_rectangle(px, py, px+self.CELL, py+self.CELL, fill="#7f8c8d")
                    if self.flags[y][x]:
                        self.canvas.create_text(px+9, py+9, text="🚩")

        if self.game_over:
            self.draw_text("GAME OVER", 84, 112, font_size=9)
        elif self.win:
            self.draw_text("YOU WIN!", 84, 112, font_size=9)
        else:
            self.draw_text("Call = odkryj | F = flaga", 84, 112, font_size=7)

    # ================= INPUT =================

    def handle_arrow(self, d):
        if self.game_over or self.win:
            return
        if d == "up": self.cursor_y = (self.cursor_y - 1) % self.GRID_H
        if d == "down": self.cursor_y = (self.cursor_y + 1) % self.GRID_H
        if d == "left": self.cursor_x = (self.cursor_x - 1) % self.GRID_W
        if d == "right": self.cursor_x = (self.cursor_x + 1) % self.GRID_W
        self.draw()

    def handle_call(self):
        if self.game_over or self.win:
            self.init_board()
            self.draw()
            return
        if self.flags[self.cursor_y][self.cursor_x]:
            return
        self.reveal(self.cursor_x, self.cursor_y)
        self.check_win()
        self.draw()

    def handle_key(self, key):
        if key.lower() == "f":
            self.toggle_flag()
            self.draw()

    # ================= GAME =================

    def toggle_flag(self):
        y, x = self.cursor_y, self.cursor_x
        if self.revealed[y][x]:
            return
        if not self.flags[y][x] and self.mines_left == 0:
            return
        self.flags[y][x] = not self.flags[y][x]
        self.mines_left += -1 if self.flags[y][x] else 1

    def reveal(self, x, y):
        if self.revealed[y][x] or self.flags[y][x]:
            return
        self.revealed[y][x] = True

        if self.board[y][x] == -1:
            self.game_over = True
            self.reveal_all()
            return

        if self.board[y][x] == 0:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < self.GRID_W and 0 <= ny < self.GRID_H:
                        self.reveal(nx, ny)

    def reveal_all(self):
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                self.revealed[y][x] = True

    def check_win(self):
        for y in range(self.GRID_H):
            for x in range(self.GRID_W):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.win = True
