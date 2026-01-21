import flet as ft
import flet.canvas as cv
import random
import time
from apps.base_app import BaseApp


class SnakeApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)

        self.grid_size = 20
        self.cell_size = 5
        self.canvas_size = self.grid_size * self.cell_size

        self.running = False
        self.reset_game()

    # ---------------- GAME STATE ----------------

    def reset_game(self):
        self.snake = [[7, 7], [7, 8], [7, 9]]
        self.direction = "up"
        self.next_direction = "up"
        self.food = self._generate_food()
        self.score = 0
        self.game_over = False

    def _generate_food(self):
        while True:
            food = [
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1),
            ]
            if food not in self.snake:
                return food

    # ---------------- UI ----------------

    # def build(self, width, height):
    #     self.score_text = ft.Text("Score: 0", size=16, weight=ft.FontWeight.BOLD)
    #     self.status_text = ft.Text("CALL=start", size=12, color="#95a5a6")
    #
    #     self.canvas = cv.Canvas(
    #         width=self.canvas_size,
    #         height=self.canvas_size,
    #         shapes=[]
    #     )
    #
    #     self.game_container = ft.Container(
    #         width=self.canvas_size,
    #         height=self.canvas_size,
    #         bgcolor="#2c3e50",
    #         border_radius=6,
    #         alignment=ft.Alignment.CENTER,
    #         content=self.canvas,
    #     )
    #
    #     layout = ft.Column(
    #         [
    #             ft.Text("SNAKE", size=20, weight=ft.FontWeight.BOLD),
    #             self.score_text,
    #             self.game_container,
    #             self.status_text,
    #         ],
    #         alignment=ft.MainAxisAlignment.CENTER,
    #         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #         spacing=5,
    #     )
    #
    #     self._draw_canvas()
    #     return layout
    #
    # # ---------------- DRAW ----------------

    def build(self, width=160, height=136):
        self.available_width = width
        self.available_height = height

        # dynamiczne dopasowanie
        self.grid_size = 10
        self.cell_size = min(
            width // self.grid_size,
            height // self.grid_size
        )

        self.canvas_size = self.grid_size * self.cell_size

        self.canvas = cv.Canvas(
            width=self.canvas_size,
            height=self.canvas_size,
            shapes=[]
        )

        self.score_text = ft.Text(
            f"Score: {self.score}",
            size=10,
            weight=ft.FontWeight.BOLD,
            color="#2c3e50",
        )

        self.status_text = ft.Text(
            "CALL=start",
            size=9,
            color="#4a5d6e",
        )

        layout = ft.Column(
            [
                self.score_text,
                ft.Container(
                    width=self.canvas_size,
                    height=self.canvas_size,
                    content=self.canvas,
                    bgcolor="#2c3e50",
                    border_radius=4,
                    alignment=ft.Alignment.CENTER,
                ),
                self.status_text,
            ],
            spacing=4,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self._draw_canvas()
        return layout

    def _draw_canvas(self):
        shapes = []

        # food
        shapes.append(
            cv.Rect(
                x=self.food[0] * self.cell_size,
                y=self.food[1] * self.cell_size,
                width=self.cell_size - 1,
                height=self.cell_size - 1,
                paint=ft.Paint(color="#e74c3c"),
                border_radius=3,
            )
        )

        # snake
        for i, seg in enumerate(self.snake):
            shapes.append(
                cv.Rect(
                    x=seg[0] * self.cell_size,
                    y=seg[1] * self.cell_size,
                    width=self.cell_size - 1,
                    height=self.cell_size - 1,
                    paint=ft.Paint(
                        color="#2ecc71" if i == 0 else "#27ae60"
                    ),
                    border_radius=2,
                )
            )

        self.canvas.shapes = shapes

    # ---------------- GAME LOOP ----------------

    async def game_loop(self):
        while self.running and not self.game_over:
            self._move_snake()
            self._draw_canvas()

            self.score_text.value = f"Score: {self.score}"
            self.phone.page.update()

            # await ft.sleep(0.15)


        if self.game_over:
            self.status_text.value = "GAME OVER! CALL=restart"
            self.phone.page.update()

    # ---------------- LOGIC ----------------

    def _move_snake(self):
        self.direction = self.next_direction
        head = self.snake[0].copy()

        if self.direction == "up":
            head[1] -= 1
        elif self.direction == "down":
            head[1] += 1
        elif self.direction == "left":
            head[0] -= 1
        elif self.direction == "right":
            head[0] += 1

        # collision
        if (
            head[0] < 0
            or head[0] >= self.grid_size
            or head[1] < 0
            or head[1] >= self.grid_size
            or head in self.snake
        ):
            self.game_over = True
            self.running = False
            return

        self.snake.insert(0, head)

        if head == self.food:
            self.score += 10
            self.food = self._generate_food()
        else:
            self.snake.pop()

    # ---------------- INPUT ----------------

    def on_arrow(self, direction):
        if direction == "up" and self.direction != "down":
            self.next_direction = "up"
        elif direction == "down" and self.direction != "up":
            self.next_direction = "down"
        elif direction == "left" and self.direction != "right":
            self.next_direction = "left"
        elif direction == "right" and self.direction != "left":
            self.next_direction = "right"

    def on_call(self):
        if self.running:
            return

        self.reset_game()
        self.running = True
        self.status_text.value = ""
        self.phone.page.run_task(self.game_loop)

    def on_back(self):
        self.running = False
        self.phone.show_menu()
