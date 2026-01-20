import tkinter as tk
from tkinter import messagebox

# Mapowanie klawiszy numerycznych na litery (jak na Nokii)
KEYPAD = {
    '0': [' ', '0'],
    '1': ['.', ',', '?', '!', '1', '-', '(', ')'],
    '2': ['a', 'b', 'c', '2'],
    '3': ['d', 'e', 'f', '3'],
    '4': ['g', 'h', 'i', '4'],
    '5': ['j', 'k', 'l', '5'],
    '6': ['m', 'n', 'o', '6'],
    '7': ['p', 'q', 'r', 's', '7'],
    '8': ['t', 'u', 'v', '8'],
    '9': ['w', 'x', 'y', 'z', '9'],
}

# Kolory Nokia 3310
BG_COLOR = '#c7f0d8'
TEXT_COLOR = '#43523d'
BUTTON_COLOR = '#a0c8b0'
SCREEN_COLOR = '#b8d8c8'


class NokiaSMS:
    def __init__(self, root):
        self.root = root
        self.root.title('Nokia 3310 - SMS')
        self.root.resizable(False, False)
        self.root.configure(bg=BG_COLOR)

        # Stan aplikacji
        self.sms_list = []  # Tablica zapisanych SMS-ów
        self.current_text = ""
        self.last_key = None
        self.key_press_count = 0
        self.typing_timer = None
        self.timeout_duration = 2000  # timeout

        self.create_ui()
        self.bind_keyboard()
        self.update_display()

    def create_ui(self):
        # Ramka główna
        main_frame = tk.Frame(self.root, bg=BG_COLOR, padx=20, pady=20)
        main_frame.pack()

        # Ekran (wyświetlacz)
        screen_frame = tk.Frame(main_frame, bg=SCREEN_COLOR, relief=tk.SUNKEN, bd=3)
        screen_frame.pack(pady=(0, 15))

        # Nagłówek
        tk.Label(
            screen_frame, text="NOWA WIADOMOŚĆ", font=('Courier', 10, 'bold'),
            bg=SCREEN_COLOR, fg=TEXT_COLOR, anchor='w'
        ).pack(fill=tk.X, padx=5, pady=(5, 0))

        # Tekst SMS
        self.text_display = tk.Text(
            screen_frame, height=5, width=30, font=('Courier', 12),
            bg=SCREEN_COLOR, fg=TEXT_COLOR, wrap=tk.WORD,
            relief=tk.FLAT, state=tk.DISABLED
        )
        self.text_display.pack(padx=5, pady=5)

        # Licznik znaków
        self.counter_label = tk.Label(
            screen_frame, text="0/160", font=('Courier', 9),
            bg=SCREEN_COLOR, fg=TEXT_COLOR, anchor='e'
        )
        self.counter_label.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Klawiatura numeryczna
        keypad_frame = tk.Frame(main_frame, bg=BG_COLOR)
        keypad_frame.pack()

        # Definicja przycisków
        buttons = [
            [('1', '.,?!'), ('2', 'abc'), ('3', 'def')],
            [('4', 'ghi'), ('5', 'jkl'), ('6', 'mno')],
            [('7', 'pqrs'), ('8', 'tuv'), ('9', 'wxyz')],
            [('*', '+'), ('0', 'space'), ('#', 'shift')],
        ]

        for row in buttons:
            row_frame = tk.Frame(keypad_frame, bg=BG_COLOR)
            row_frame.pack()
            for num, letters in row:
                self.create_button(row_frame, num, letters)

        # Przyciski funkcyjne
        func_frame = tk.Frame(main_frame, bg=BG_COLOR)
        func_frame.pack(pady=(10, 0))

        tk.Button(
            func_frame, text="◀ Usuń", command=self.backspace,
            font=('Arial', 10), bg=BUTTON_COLOR, fg=TEXT_COLOR,
            width=12, height=2, relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            func_frame, text="✓ Zapisz SMS", command=self.save_sms,
            font=('Arial', 10, 'bold'), bg=BUTTON_COLOR, fg=TEXT_COLOR,
            width=12, height=2, relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            func_frame, text="📋 Skrzynka", command=self.show_saved_sms,
            font=('Arial', 10), bg=BUTTON_COLOR, fg=TEXT_COLOR,
            width=12, height=2, relief=tk.RAISED
        ).pack(side=tk.LEFT, padx=5)

        # Instrukcja
        info_text = "Klikaj cyfry wielokrotnie aby wybrać literę | # = wielka litera | 3 sek. timeout"
        tk.Label(
            main_frame, text=info_text, font=('Arial', 8),
            bg=BG_COLOR, fg=TEXT_COLOR, wraplength=500
        ).pack(pady=(10, 0))

    def create_button(self, parent, num, letters):
        btn_frame = tk.Frame(parent, bg=BG_COLOR)
        btn_frame.pack(side=tk.LEFT, padx=3, pady=3)

        btn = tk.Button(
            btn_frame, text=num, font=('Arial', 16, 'bold'),
            bg=BUTTON_COLOR, fg=TEXT_COLOR,
            width=5, height=2, relief=tk.RAISED,
            command=lambda n=num: self.key_press(n)
        )
        btn.pack()

        lbl = tk.Label(
            btn_frame, text=letters, font=('Arial', 7),
            bg=BG_COLOR, fg=TEXT_COLOR
        )
        lbl.pack()

    def bind_keyboard(self):
        """Bindowanie klawiatury komputera"""
        for i in range(10):
            self.root.bind(str(i), lambda e, n=str(i): self.key_press(n))
        self.root.bind('#', lambda e: self.shift_case())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        self.root.bind('<Return>', lambda e: self.save_sms())

    def key_press(self, key):
        """Obsługa naciśnięcia klawisza - GŁÓWNA LOGIKA"""
        if key not in KEYPAD:
            return

        # Jeśli naciśnięto INNY klawisz niż ostatnio - zatwierdź poprzedni znak
        if key != self.last_key and self.last_key is not None:
            self.confirm_current_char()

        # Anuluj poprzedni timer
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)

        # Jeśli to ten sam klawisz - przełącz na następną literę
        if key == self.last_key:
            self.key_press_count += 1
            # Usuń ostatnią literę (będziemy ją zastępować następną)
            if self.current_text:
                self.current_text = self.current_text[:-1]
        else:
            # Nowy klawisz - zaczynamy od pierwszej litery
            self.key_press_count = 0
            self.last_key = key

        # Pobierz dostępne znaki dla tego klawisza
        chars = KEYPAD[key]
        char_index = self.key_press_count % len(chars)
        char = chars[char_index]

        # Dodaj znak
        self.current_text += char
        self.update_display()

        # Ustaw timer - po 3 sekundach zatwierdź znak i przejdź dalej
        self.typing_timer = self.root.after(self.timeout_duration, self.confirm_current_char)

    def confirm_current_char(self):
        """Zatwierdź aktualny znak i zresetuj stan"""
        self.last_key = None
        self.key_press_count = 0
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
            self.typing_timer = None

    def shift_case(self):
        """Zmień wielkość ostatniej litery (klawisz #)"""
        if self.current_text:
            last_char = self.current_text[-1]
            if last_char.isalpha():
                if last_char.isupper():
                    self.current_text = self.current_text[:-1] + last_char.lower()
                else:
                    self.current_text = self.current_text[:-1] + last_char.upper()
                self.update_display()

    def backspace(self):
        """Usuń ostatni znak"""
        if self.current_text:
            self.current_text = self.current_text[:-1]
            self.confirm_current_char()  # Zresetuj stan
            self.update_display()

    def update_display(self):
        """Odśwież wyświetlacz"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(1.0, self.current_text)
        self.text_display.config(state=tk.DISABLED)

        # Licznik znaków
        char_count = len(self.current_text)
        self.counter_label.config(text=f"{char_count}/160")

    def save_sms(self):
        """Zapisz SMS do tablicy"""
        if not self.current_text.strip():
            messagebox.showwarning("Uwaga", "SMS jest pusty!")
            return

        # Zatwierdź aktualny znak przed zapisaniem
        self.confirm_current_char()

        self.sms_list.append(self.current_text.strip())
        messagebox.showinfo("Zapisano", f"SMS zapisany!\nLiczba SMS-ów: {len(self.sms_list)}")

        # Wyczyść ekran
        self.current_text = ""
        self.update_display()

    def show_saved_sms(self):
        """Pokaż zapisane SMS-y"""
        if not self.sms_list:
            messagebox.showinfo("Skrzynka", "Brak zapisanych SMS-ów")
            return

        # Okno z listą SMS-ów
        sms_window = tk.Toplevel(self.root)
        sms_window.title("Zapisane SMS-y")
        sms_window.configure(bg=BG_COLOR)
        sms_window.geometry("500x400")

        tk.Label(
            sms_window, text=f"ZAPISANE SMS-Y ({len(self.sms_list)})",
            font=('Arial', 14, 'bold'), bg=BG_COLOR, fg=TEXT_COLOR
        ).pack(pady=10)

        # Ramka z scrollbarem
        frame = tk.Frame(sms_window, bg=BG_COLOR)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista SMS-ów
        text_widget = tk.Text(
            frame, font=('Courier', 10),
            bg=SCREEN_COLOR, fg=TEXT_COLOR, wrap=tk.WORD,
            yscrollcommand=scrollbar.set
        )
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=text_widget.yview)

        for i, sms in enumerate(self.sms_list, 1):
            text_widget.insert(tk.END, f"─── SMS {i} ───\n")
            text_widget.insert(tk.END, f"{sms}\n\n")

        text_widget.config(state=tk.DISABLED)

        tk.Button(
            sms_window, text="Zamknij", command=sms_window.destroy,
            font=('Arial', 10), bg=BUTTON_COLOR, fg=TEXT_COLOR,
            width=15, height=2
        ).pack(pady=(0, 10))


if __name__ == '__main__':
    root = tk.Tk()
    app = NokiaSMS(root)
    root.mainloop()