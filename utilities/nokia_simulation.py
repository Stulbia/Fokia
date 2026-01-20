import tkinter as tk
from tkinter import Canvas
import random


class Nokia3310:
    def __init__(self, root):
        self.root = root
        self.root.title("Nokia 3310 Simulator")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)

        # Calculator state
        self.menu = False
        self.menu_list=["sms","","game","calculator","ringtone"]
        self.menu_selected = 1



        if self.menu == True:
            self.draw_menu_screen()


        self.calc_display = ""
        self.calc_result = ""



        # Snake game state
        self.snake_running = False
        self.snake_body = [(5, 5), (5, 4), (5, 3)]
        self.snake_direction = (0, 1)
        self.food = (10, 10)
        self.score = 0

        # Current mode
        self.mode = "calculator"  # or "snake"

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#34495e', bd=10, relief='raised')
        main_frame.pack(padx=20, pady=20)

        # logo
        logo_frame = tk.Frame(main_frame, bg='#34495e', height=30)
        logo_frame.pack(fill='x', pady=(5, 10))
        logo = tk.Label(logo_frame, text="FOKIA", font=('Comic Sans', 16, 'bold'),
                        bg='#34495e', fg='#7f8c8d')
        logo.pack()

        # Screen
        screen_frame = tk.Frame(main_frame, bg='#1a1a1a', bd=3, relief='sunken')
        screen_frame.pack(pady=10, padx=15)
        self.screen = Canvas(screen_frame, width=168, height=100,
                             bg='#9db88a', highlightthickness=0)
        self.screen.pack(padx=2, pady=2)

        #first diplay
        self.update_screen()


        # frame for buttons and stuff
        controls_frame = tk.Frame(main_frame, bg='#34495e')
        controls_frame.pack(pady=10)
        # D-pad

        center_btn = tk.Button(controls_frame, text="OK", width=6, height=1,
                               font=('Arial', 10, 'bold'), bg='#7f8c8d',
                               relief='raised', bd=3, command=self.center_press)
        center_btn.grid(row=2, column=1, padx=5, pady=5)


        up_btn = tk.Button(controls_frame, text="▲", width=6, height=1,
                           font=('Arial', 12), bg='#95a5a6', relief='raised', bd=3,
                           command=lambda: self.arrow_press("up"))
        up_btn.grid(row=1, column=1)

        down_btn = tk.Button(controls_frame, text="▼", width=6, height=1,
                             font=('Arial', 12), bg='#95a5a6', relief='raised', bd=3,
                             command=lambda: self.arrow_press("down"))
        down_btn.grid(row=3, column=1)

        left_btn = tk.Button(controls_frame, text="◄", width=3, height=1,
                             font=('Arial', 12), bg='#95a5a6', relief='raised', bd=3,
                             command=lambda: self.arrow_press("left"))
        left_btn.grid(row=2, column=0)

        right_btn = tk.Button(controls_frame, text="►", width=3, height=1,
                              font=('Arial', 12), bg='#95a5a6', relief='raised', bd=3,
                              command=lambda: self.arrow_press("right"))
        right_btn.grid(row=2, column=2)

        # Numpad keyboard
        keypad_frame = tk.Frame(main_frame, bg="blue")
        keypad_frame.pack()

        # buttons defined
        buttons = [
            [('1', '.,?!'), ('2', 'abc'), ('3', 'def')],
            [('4', 'ghi'), ('5', 'jkl'), ('6', 'mno')],
            [('7', 'pqrs'), ('8', 'tuv'), ('9', 'wxyz')],
            [('*', '+'), ('0', 'space'), ('#', 'shift')],
        ]

        for row in buttons:
            row_frame = tk.Frame(keypad_frame, bg="blue")
            row_frame.pack()
            for num, letters in row:
                self.create_button(row_frame, num, letters)

        # Call/End buttons
        call_frame = tk.Frame(main_frame, bg='#34495e')
        call_frame.pack(pady=10)

        call_btn = tk.Button(call_frame, text="📞", width=8, height=1,
                             font=('Arial', 14), bg='#27ae60', fg='white',
                             relief='raised', bd=3, command=self.call_press)
        call_btn.grid(row=0, column=0, padx=5)

        end_btn = tk.Button(call_frame, text="✖", width=8, height=1,
                            font=('Arial', 14), bg='#c0392b', fg='white',
                            relief='raised', bd=3, command=self.end_press)
        end_btn.grid(row=0, column=1, padx=5)

    # def create_button(self, parent, text, row, col, command):
    #     btn = tk.Button(parent, text=text, width=6, height=1,
    #                     font=('Arial', 10, 'bold'), bg='#bdc3c7',
    #                     relief='raised', bd=3, command=command)
    #     btn.grid(row=row, column=col, padx=3, pady=3)
    #     return btn

    def create_button(self, parent, num, letters):
        # Tworzymy ramkę dla pojedynczego przycisku, żeby ładnie wyglądał
        btn_text = f"{num}\n{letters}"
        button = tk.Button(parent, text=btn_text, width=5, height=2,
                           font=('Arial', 10), bg='#ecf0f1',
                           command=lambda n=num: self.numpad_press(n))
        # UŻYWAMY .pack(), bo row_frame (parent) będzie zarządzany przez .pack() w pętli
        button.pack(side='left', padx=2, pady=2)


    def update_screen(self):
        self.screen.delete("all")
        # if self.mode == "calculator":
        #     # self.draw_calculator_screen()
        # elif self.mode == "snake":
        #     # self.draw_snake_screen()
        # elif self.mode == "home":
        self.draw_home_screen()

    def draw_menu_screen(self):
        self.mode = self.menu_list[self.menu_selected]
        return

    def draw_home_screen(self):
        if self.center_press():
            self.menu=True
            self.draw_menu_screen()



    # def draw_calculator_screen(self):


    # def draw_snake_screen(self):

    def arrow_press(dd):
        return dd

    def center_press(dd):
        return dd
    def call_press(dd):
        return dd

    def end_press(dd):
        return dd


if __name__ == "__main__":
    root = tk.Tk()
    app = Nokia3310(root)
    root.mainloop()