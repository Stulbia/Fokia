class BaseScreen:

    def __init__(self, canvas, screen_manager):
        self.canvas = canvas
        self.screen_manager = screen_manager
        self.running = True

#draws the screen - to be implemented in inheriting classes
    def draw(self):
        self.canvas.delete("all")
#stops screen from runnng - ex. timers, animations etc.
    def stop(self):
        self.running = False

#button handling templates
    def handle_arrow(self, direction):
        pass

    def handle_center(self):
        pass

    def handle_numpad(self, key):
        pass

    def handle_call(self):
        pass

    def handle_end(self):
        return False

#just makes text appear coherent
    def draw_text(self, text, x, y, font_size=10, anchor="center"):

        self.canvas.create_text(x, y, text=text,
                                font=('Arial', font_size),
                                fill='#1a1a1a', anchor=anchor)
#basic brush
    def draw_rectangle(self, x1, y1, x2, y2, fill="black", outline=""):
        self.canvas.create_rectangle(x1, y1, x2, y2,
                                     fill=fill, outline=outline)