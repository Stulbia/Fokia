import tkinter as tk
from tkinter import Canvas
from tkinter import ttk

class PhoneUI:
    def __init__(self, root):
        self.root = root
        self.BASE_W, self.BASE_H = 350, 700
        self.scale_factor = 1.0
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' supports better border editing
        self.style.configure("Rounded.TButton",
                             relief="flat",
                             background="#8ee6fa",
                             borderwidth=1,
                             focusthickness=3,
                             focuscolor='none',
                             corner_radius=20,)
        self.all_buttons = []
        self.keypad_buttons = {}

        self.create_widgets()
        self.root.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        if event.widget == self.root:
            self.scale_factor = max(0.4, min(event.width / self.BASE_W, event.height / self.BASE_H))
            self._update_ui_scale()

    def _update_ui_scale(self):
        s = self.scale_factor
        # self.logo_label.config(font=('Helvetica', int(20 * s), 'bold'))
        self.screen.config(width=int(240 * s), height=int(190 * s))

        btn_font = ('Arial', int(11 * s), 'bold')
        # for btn in self.all_buttons:
            # btn.config(font=btn_font)

    def create_widgets(self):
        # Outer "Spacer" frame that will be transparent
        self.outer_container = tk.Frame(self.root, bg='#1a1a1a', padx=10, pady=10)
        self.outer_container.pack(expand=True, fill='both')
        # Main Body
        self.phone_body = tk.Frame(self.root, bg='#2C3E50')
        self.phone_body.pack(expand=True, fill='both')

        self.logo_label = tk.Label(self.phone_body, text="FOKIA", bg='#2C3E50', fg='#ECF0F1')
        self.logo_label.pack(pady=(15, 5))

        # Screen
        screen_border = tk.Frame(self.phone_body, bg='#1A1A1A', bd=4, relief='sunken')
        screen_border.pack(pady=10)
        self.screen = Canvas(screen_border, bg='#9db88a', highlightthickness=0)
        self.screen.pack(padx=5, pady=5)

        # Controls (D-Pad)
        dpad_frame = tk.Frame(self.phone_body, bg='#2C3E50')
        dpad_frame.pack(pady=5)
        self.up_btn = self._add_btn(dpad_frame, "▲", 0, 1)
        self.left_btn = self._add_btn(dpad_frame, "◄", 1, 0)
        self.center_btn = self._add_btn(dpad_frame, "OK", 1, 1, color='#BDC3C7')
        self.right_btn = self._add_btn(dpad_frame, "►", 1, 2)
        self.down_btn = self._add_btn(dpad_frame, "▼", 2, 1)

        # Keypad
        self.keypad_frame = tk.Frame(self.phone_body, bg='#2C3E50')
        self.keypad_frame.pack(expand=True, fill='both', padx=30, pady=10)
        for i in range(3): self.keypad_frame.columnconfigure(i, weight=1)
        for i in range(4): self.keypad_frame.rowconfigure(i, weight=1)

        keys = [('1', '.,'), ('2', 'ABC'), ('3', 'DEF'), ('4', 'GHI'), ('5', 'JKL'), ('6', 'MNO'),
                ('7', 'PQRS'), ('8', 'TUV'), ('9', 'WXYZ'), ('*', '+'), ('0', '_'), ('#', '⇧')]

        for i, (num, sub) in enumerate(keys):
            btn = ttk.Button(self.keypad_frame, text=f"{num}\n{sub}", style="Rounded.TButton")
            btn.grid(row=i // 3, column=i % 3, sticky="nsew", padx=2, pady=2)
            self.keypad_buttons[num] = btn
            self.all_buttons.append(btn)

        # Action Buttons
        action_frame = tk.Frame(self.phone_body, bg='#2C3E50')
        action_frame.pack(fill='x', padx=30, pady=(0, 20))
        action_frame.columnconfigure(0, weight=1)
        action_frame.columnconfigure(1, weight=1)

        self.call_btn = ttk.Button(action_frame, text="CALL", style="Rounded.TButton")
        self.call_btn.grid(row=0, column=0, padx=5, sticky="nsew")
        self.end_btn = ttk.Button(action_frame, text="END", style="Rounded.TButton")
        self.end_btn.grid(row=0, column=1, padx=5, sticky="nsew")
        self.all_buttons.extend([self.call_btn, self.end_btn])

    def _add_btn(self, parent, txt, r, c, color='#95A5A6'):
        btn = ttk.Button(parent, text=txt, style="Rounded.TButton")
        btn.grid(row=r, column=c, padx=2, pady=2)
        self.all_buttons.append(btn)
        return btn

    def set_callbacks(self, arrow_callback, center_callback, numpad_callback, call_callback, end_callback):
        self.up_btn.config(command=lambda: arrow_callback("up"))
        self.down_btn.config(command=lambda: arrow_callback("down"))
        self.left_btn.config(command=lambda: arrow_callback("left"))
        self.right_btn.config(command=lambda: arrow_callback("right"))
        self.center_btn.config(command=center_callback)
        for key, btn in self.keypad_buttons.items():
            btn.config(command=lambda k=key: numpad_callback(k))
        self.call_btn.config(command=call_callback)
        self.end_btn.config(command=end_callback)