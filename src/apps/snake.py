import flet as ft
import flet.canvas as cv
import random
import asyncio
from src.apps.base_app import BaseApp


class SnakeApp(BaseApp):
    def __init__(self, phone):
        super().__init__(phone)
        self.grid_size = 12
        self.cell_size = 8
        self.canvas_size = self.grid_size * self.cell_size
        self.running = False
        self.game_speed = 0.5 # Seconds Per Frame
        self.pending_update = False
        self.reset_game()

    def reset_game(self):
        center = self.grid_size // 2
        self.snake = [[center, center], [center, center + 1], [center, center + 2]]
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

    def build(self, width, height):
        #Compability screen size
        header_height = 20
        footer_height = 20
        spacing_total = 10
        canvas_available = height - header_height - footer_height - spacing_total

        # Grid adjustments
        max_cell_size = min(
            (width - 10) // self.grid_size,
            canvas_available // self.grid_size
        )
        self.cell_size = max(6, min(max_cell_size, 10))
        self.canvas_size = self.grid_size * self.cell_size

        self.canvas = cv.Canvas(
            width=self.canvas_size,
            height=self.canvas_size,
            shapes=[]
        )

        self.score_text = ft.Text(
            f"Score: {self.score}",
            size=11,
            weight=ft.FontWeight.BOLD,
            color="#2c3e50",
        )

        self.status_text = ft.Text(
            "CALL = start",
            size=8,
            color="#7f8c8d",
        )

        layout = ft.Container(
            width=width,
            height=height,
            content=ft.Column(
                controls=[
                    # Header
                    ft.Container(
                        content=self.score_text,
                        height=header_height,
                        alignment=ft.Alignment.CENTER,
                    ),

                    # Game canvas
                    ft.Container(
                        width=self.canvas_size,
                        height=self.canvas_size,
                        content=self.canvas,
                        bgcolor="#a4b494",
                        border_radius=4,
                        alignment=ft.Alignment.CENTER,
                        border=ft.border.all(1, "#1a1a1a"),
                    ),

                    # Footer
                    ft.Container(
                        content=self.status_text,
                        height=footer_height,
                        alignment=ft.Alignment.CENTER,
                    ),
                ],
                spacing=5,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        self._draw_canvas()
        return layout

    def _draw_canvas(self):
        shapes = []

        # Apples
        food_margin = 1
        shapes.append(
            cv.Rect(
                x=self.food[0] * self.cell_size + food_margin,
                y=self.food[1] * self.cell_size + food_margin,
                width=self.cell_size - food_margin * 2,
                height=self.cell_size - food_margin * 2,
                paint=ft.Paint(color="#3b3d39"),
                border_radius=self.cell_size // 3,
            )
        )

        # Snake - head and body
        snake_margin = 1
        for i, seg in enumerate(self.snake):
            is_head = i == 0
            shapes.append(
                cv.Rect(
                    x=seg[0] * self.cell_size + snake_margin,
                    y=seg[1] * self.cell_size + snake_margin,
                    width=self.cell_size - snake_margin * 2,
                    height=self.cell_size - snake_margin * 2,
                    paint=ft.Paint(
                        color="000000" if is_head else "#2e2e2e"
                    ),
                    border_radius=2,
                )
            )

        self.canvas.shapes = shapes

    async def game_loop(self):
        while self.running and not self.game_over:
            self._move_snake()
            self._draw_canvas()

            # Batch update (once per tick)
            self.score_text.value = f"Score: {self.score}"

            try:
                self.phone.page.update()
            except:
                break

            await asyncio.sleep(self.game_speed)

        if self.game_over:
            self.status_text.value = "END!  CALL = restart"
            self.running = False
            try:
                self.phone.page.update()
            except:
                pass

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

        # handle Collisions
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

        # Eating
        if head == self.food:
            self.score += 10
            self.food = self._generate_food()
            # I AM SPEED
            if self.game_speed > 0.08:
                self.game_speed *= 0.98
        else:
            self.snake.pop()

    def on_arrow(self, direction):
        # no 180 degrees
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
        self.game_speed = 0.5  # Reset speed
        self.running = True
        self.status_text.value = "↑↓←→"
        self._draw_canvas()
        self.phone.page.update()

        # Use run_task from asyncio
        asyncio.create_task(self.game_loop())

    def on_back(self):
        self.running = False
        self.phone.show_menu()