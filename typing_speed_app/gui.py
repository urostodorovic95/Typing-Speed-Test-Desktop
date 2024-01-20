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
    ROUNDS_DURATION_MS = 10000
    # Styling
    FONT = ("Helvetica", 40)
    BG_COLOR = "#AAD7D9"
    FG_COLOR = "#FBF9F1"

    def __init__(self, parent):
        super().__init__(parent)

        # self.generated_words = self.get_random_words()
        self.generated_words = "hello world"
        self.uncorrected_round_mistakes = []

        self.bank_text_display = tk.Text(master=parent, wrap="none", width=50, height=1)
        self.bank_text_display.grid(row=0, column=0, padx=(5, 5), pady=(10, 10))
        self.bank_text_display.insert(index="1.0", chars=self.generated_words)
        self.bank_text_display.configure(
            bg=self.BG_COLOR, font=self.FONT, foreground=self.FG_COLOR, padx=0, pady=40
        )
        # make it read-only
        self.bank_text_display.bind("<Key>", lambda event: "break")
        # tags
        self.bank_text_display.tag_configure("center", justify="center")
        self.bank_text_display.tag_configure(
            "red", foreground="#ED5AB3"
        )  # When a mistake is made

        self.bank_text_display.tag_add("center", "1.0", "end")

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
        self.after(MainFrame.ROUNDS_DURATION_MS, self.finish_test)

    def finish_test(self):
        # calculate score
        # reset screen
        # display score and stats
        # ask for another round?
        pass

    @staticmethod
    def discard_extra_text(user_text: str, compared_to: str) -> str:
        if user_text:
            if len(user_text) > len(compared_to):
                return user_text[: len(compared_to) - 1]
        return user_text

    def evaluate_last_input(self, event):
        computer_text = self.bank_text_display.get("1.0", "end")
        user_text = self.discard_extra_text(self.user_entry.get(), computer_text)
        evaluate_input = AppBrain(computer_text=computer_text, user_text=user_text)

        if not evaluate_input.is_round_over():
            if evaluate_input.is_last_char_same():
                print("true")
                self.remove_red_color(evaluate_input)
            else:
                self.add_red_color(evaluate_input)
        else:
            print("round over")
            self.uncorrected_round_mistakes.append(
                self.evaluate_round_mistakes(evaluate_input)
            )
            print(self.uncorrected_round_mistakes)
            print(computer_text)
            print(user_text)
            self.reset_round()

    def add_red_color(self, brain_object):
        self.bank_text_display.tag_add("red", f"1.{brain_object.last_index}")

    def remove_red_color(self, brain_object):
        self.bank_text_display.tag_remove("red", f"1.{brain_object.last_index}")

    def evaluate_round_mistakes(self, brain_object):
        return brain_object.count_round_errors()

    def reset_round(self):
        self.bank_text_display.delete("1.0", "end")
        self.generated_words = self.get_random_words()
        self.bank_text_display.insert("1.0", self.generated_words)
        self.bank_text_display.tag_add("center", "1.0", "end")
        self.user_entry.delete(0, "end")


# debug
app = AppWindow()
MainFrame(parent=app)
app.mainloop()
