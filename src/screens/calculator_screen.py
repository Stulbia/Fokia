from screens.base_screen import BaseScreen


class CalculatorScreen(BaseScreen):

    def __init__(self, canvas, screen_manager):
        super().__init__(canvas, screen_manager)

        # Display & state
        self.display = ""
        self.result = ""
        self.sign = ""

        # Operands
        self.left = None
        self.right = None

    # ================= DRAW =================

    def draw(self):
        super().draw()

        # Title
        self.draw_text("CALCULATOR", 84, 15, font_size=10)
        self.canvas.create_line(10, 25, 158, 25, fill='#1a1a1a', width=1)

        # Main display
        display_text = self.display if self.display else "0"
        self.draw_text(display_text, 158, 40, font_size=12, anchor="e")

        # Result display
        if self.result:
            self.canvas.create_line(10, 55, 158, 55, fill='#1a1a1a', width=1)
            self.draw_text(self.result, 158, 70, font_size=16, anchor="e")

        # Instructions
        self.draw_text("Use numeric keypad", 84, 95, font_size=7)
        self.draw_text("# = wynik, * = czyść", 84, 105, font_size=6)

    # ================= INPUT =================

    def handle_numpad(self, key):
        if key == '*':  # clear
            self.clear()
            return

        if key.isdigit():
            self.display += key

        self.draw()

    def handle_arrow(self, direction):
        # Do not allow operator at the start or multiple operators
        if not self.display or self.sign:
            return

        match direction:
            case "up":
                self.sign = "+"
            case "down":
                self.sign = "-"
            case "left":
                self.sign = "*"
            case "right":
                self.sign = "/"
            case _:
                return

        self.left = float(self.display)
        self.display += f" {self.sign} "
        self.draw()

    def handle_call(self):
        """Call = calculate"""
        self.calculate()

    def handle_end(self):
        """End = exit calculator"""
        return False

    # ================= LOGIC =================

    def clear(self):
        self.display = ""
        self.result = ""
        self.sign = ""
        self.left = None
        self.right = None
        self.draw()

    def calculate(self):
        try:
            if not self.sign:
                return

            parts = self.display.split()
            if len(parts) != 3:
                return

            self.left = float(parts[0])
            self.right = float(parts[2])

            match self.sign:
                case "+":
                    value = self.left + self.right
                case "-":
                    value = self.left - self.right
                case "*":
                    value = self.left * self.right
                case "/":
                    if self.right == 0:
                        raise ZeroDivisionError
                    value = self.left / self.right

            self.result = self.format_result(value)

        except ZeroDivisionError:
            self.result = "DIV BY 0"
        except Exception:
            self.result = "ERROR"

        self.draw()

    def format_result(self, value):
        if value.is_integer():
            return str(int(value))
        return f"{value:.2f}"
