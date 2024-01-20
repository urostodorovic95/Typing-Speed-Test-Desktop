import tkinter as tk
from tkinter import ttk
from words_generator import generate_words
from appbrain import AppBrain


class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typing Speed Test")
        self.size = "800x400"
        self.resizable = (False, False)
        self.configure(background="#EEF5FF")

    def __repr__(self) -> str:
        return f"Subclass {AppWindow} of {super().__repr__()}"


class MainFrame(ttk.Frame):
    WORDS_PER_ROUND = 6
    # Styling
    FONT = ("Helvetica", 30)
    BG_COLOR = "#AAD7D9"
    FG_COLOR = "#FBF9F1"

    def __init__(self, parent):
        super().__init__(parent)

        self.generated_words = self.get_random_words()

        self.bank_text_display = tk.Text(master=parent, wrap="none", width=50, height=1)
        self.bank_text_display.grid(row=0, column=0, padx=(5, 5), pady=(10, 10))
        self.bank_text_display.insert(index="1.0", chars=self.generated_words)
        self.bank_text_display.configure(
            bg=self.BG_COLOR, font=self.FONT, foreground=self.FG_COLOR, padx=0, pady=40
        )
        # tags
        self.bank_text_display.tag_configure("center", justify="center")
        self.bank_text_display.tag_configure(
            "red", foreground="#ED5AB3"
        )  # When a mistake is made

        self.bank_text_display.tag_add("center", "1.0", "end")
        self.bank_text_display.tag_add("red", "1.4")

        # entry widget
        self.user_entry = ttk.Entry(
            master=parent, background=self.FG_COLOR, foreground=self.BG_COLOR
        )
        self.user_entry.focus()
        self.entry_placeholder = "Click here and start typing!"
        self.user_entry.configure(width=len(self.entry_placeholder) - 9)
        self.user_entry.insert(0, self.entry_placeholder)
        self.user_entry.grid(row=1, column=0, pady=(20, 10))
        self.user_entry.bind("<ButtonRelease-1>", self.game_init)
        self.user_entry.bind("<KeyRelease>", self.evaluate_last_input)

    @staticmethod
    def get_random_words(n_words=WORDS_PER_ROUND) -> str:
        return generate_words(n_words)

    def delete_widget_text(self):
        if self.user_entry.get() == self.entry_placeholder:
            self.user_entry.delete(0, "end")

    def game_init(self, event):
        self.delete_widget_text()

    def evaluate_last_input(self, event):
        evaluate_input = AppBrain(
            computer_text=self.bank_text_display.get("1.0", "end"),
            user_text=self.user_entry.get(),
        )
        if not evaluate_input.is_round_over():
            if evaluate_input.is_last_char_same():
                print("true")
            else:
                print("false")
        else:
            print("round over")


# debug
app = AppWindow()
MainFrame(parent=app)
app.mainloop()
