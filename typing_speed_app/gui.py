import tkinter as tk
from tkinter import ttk
from words_generator import generate_words


class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typing Speed Test")
        self.size = "800x400"
        self.resizable = (False, False)

    def __repr__(self) -> str:
        return f"Subclass {AppWindow} of {super().__repr__()}"


class MainFrame(ttk.Frame):
    WORDS_PER_ROUND = 5

    def __init__(self, parent):
        super().__init__(parent)

        self.bank_text_display = tk.Text(
            master=parent, wrap="word", width=50, height=10
        )
        self.bank_text_display.grid(row=0, column=0)
        self.bank_text_display.insert(index="1.0", chars=self.get_random_words())

    @staticmethod
    def get_random_words(words=WORDS_PER_ROUND):
        return generate_words(words)


# debug
app = AppWindow()
MainFrame(parent=app)
app.mainloop()
