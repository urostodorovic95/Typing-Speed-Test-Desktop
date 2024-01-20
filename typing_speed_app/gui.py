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
    WORDS_PER_ROUND = 6
    # Styling
    FONT = ("Helvetica", 30)

    def __init__(self, parent):
        super().__init__(parent)

        self.generated_words = self.get_random_words()

        self.bank_text_display = tk.Text(master=parent, wrap="none", width=50, height=1)
        self.bank_text_display.grid(row=0, column=0)
        self.bank_text_display.insert(index="1.0", chars=self.generated_words)
        self.bank_text_display.configure(
            bg="#AAD7D9", font=self.FONT, foreground="#FBF9F1", padx=0, pady=40
        )
        # tags
        self.bank_text_display.tag_configure("center", justify="center")
        self.bank_text_display.tag_configure(
            "red", foreground="#ED5AB3"
        )  # When a mistake is made

        self.bank_text_display.tag_add("center", "1.0", "end")
        self.bank_text_display.tag_add("red", "1.4")

    @staticmethod
    def get_random_words(words=WORDS_PER_ROUND):
        return generate_words(words)


# debug
app = AppWindow()
MainFrame(parent=app)
app.mainloop()
