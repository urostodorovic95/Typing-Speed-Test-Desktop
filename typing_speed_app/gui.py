import tkinter as tk
from tkinter import ttk
from .words_generator import generate_words
from .appbrain import AppBrain
from .graphical_timer import CountdownTimer


class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Typing Speed Test")
        self.geometry("1000x600")
        self.resizable = (False, False)
        self.configure(background="#EEF5FF")
        self.rowconfigure(0, weight=5)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

    def __repr__(self) -> str:
        return f"Subclass {AppWindow} of {super().__repr__()}"


class MainFrame(ttk.Frame):
    WORDS_PER_ROUND = 5
    ROUNDS_DURATION_MS = 60000
    # Styling
    FONT = ("Helvetica", 35)
    BG_COLOR = "#AAD7D9"
    FG_COLOR = "#FBF9F1"
    RED_COLOR_STYLED = "#ED5AB3"

    def __init__(self, parent):
        super().__init__(parent)

        self.generated_words = self.get_random_words()
        self.uncorrected_round_mistakes = []
        self.typed_chars = ""
        self.test_initialized_id = None
        self.test_initialized = False
        self.computer_text = ""
        self.user_text = ""

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
            "red", foreground=MainFrame.RED_COLOR_STYLED
        )  # When a mistake is made

        self.bank_text_display.tag_add("center", "1.0", "end")

        # entry widget
        self.user_entry = ttk.Entry(
            master=parent, background=self.FG_COLOR, foreground=self.BG_COLOR
        )
        self.user_entry.focus()
        self.entry_placeholder = "Click here and start typing!"
        self.user_entry.configure(
            width=len(self.entry_placeholder) - 9, font="Helvetica, 30"
        )
        self.user_entry.insert(0, self.entry_placeholder)
        self.user_entry.grid(row=1, column=0, pady=(20, 10))
        self.user_entry.bind("<ButtonRelease-1>", self.game_init)
        self.user_entry.bind("<KeyRelease>", self.evaluate_last_input)

        # countdown timer
        timer_label = tk.Label(parent, text="Time left:")
        timer_label.configure(
            background="#E5E1DA", font=("Helvetica", 20, "italic"), foreground="#0F1035"
        )
        self.progress_style = ttk.Style()
        self.progress_style.theme_use("clam")
        self.progress_style.configure(
            "red.Horizontal.TProgressbar",
            thickness=50,
            foreground="#B4D4FF",
            background="#365486",
        )

        timer_progressbar = ttk.Progressbar(
            parent,
            orient="horizontal",
            length=400,
            mode="determinate",
            maximum=100,
            style="red.Horizontal.TProgressbar",
        )
        timer_progressbar["value"] = 100
        self.timer = CountdownTimer(
            time_ms=MainFrame.ROUNDS_DURATION_MS,
            parent=parent,
            label=timer_label,
            progressbar=timer_progressbar,
        )
        self.timer.label.grid(row=2, column=0, pady=10)
        self.timer.progress.grid(row=3, column=0, pady=(5, 10))

    @staticmethod
    def get_random_words(n_words=WORDS_PER_ROUND) -> str:
        return generate_words(n_words)

    def delete_widget_text(self):
        if self.user_entry.get() == self.entry_placeholder:
            self.user_entry.delete(0, "end")

    def game_init(self, event):
        self.timer.init_timer()
        if not self.test_initialized:
            self.delete_widget_text()
            self.test_initialized_id = self.after(
                MainFrame.ROUNDS_DURATION_MS, self.finish_test
            )

    def finish_test(self):
        self.after_cancel(self.test_initialized_id)
        self.test_initialized = True
        self.user_entry.delete(0, "end")
        self.user_entry.configure(state="disabled")
        # properly handle mistakes if timer reaches 0
        self.uncorrected_round_mistakes.append(
            self.evaluate_round_mistakes(
                AppBrain(computer_text=self.computer_text, user_text=self.user_text)
            )
        )
        print(self.uncorrected_round_mistakes)
        # display score and stats
        wpm, errors = self.process_score()
        self.bank_text_display.delete("1.0", "end")
        self.bank_text_display.tag_delete("red")
        message = (
            f"Test over! Your typing speed is {wpm} WPM. Average errors: {errors}."
        )
        self.bank_text_display.insert("1.0", message)
        self.bank_text_display.tag_add("center", "1.0", "end")
        self.bank_text_display.configure(font=("Helvetica", 30))

    @staticmethod
    def discard_extra_text(user_text: str, compared_to: str) -> str:
        if user_text:
            if len(user_text) > len(compared_to):
                return user_text[: len(compared_to) - 1]
        return user_text

    def evaluate_last_input(self, event):
        typed_char = event.keysym
        if typed_char == "space":
            typed_char = " "
        self.typed_chars = self.typed_chars + typed_char
        self.computer_text = self.bank_text_display.get("1.0", "end")
        self.user_text = self.discard_extra_text(
            self.user_entry.get(), self.computer_text
        )
        evaluate_input = AppBrain(
            computer_text=self.computer_text, user_text=self.user_text
        )

        if not evaluate_input.is_round_over():
            if evaluate_input.is_last_char_same():
                self.remove_red_color(evaluate_input)
            else:
                self.add_red_color(evaluate_input)
        else:
            self.uncorrected_round_mistakes.append(
                self.evaluate_round_mistakes(evaluate_input)
            )
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

    def process_score(self):
        average_error_count = sum(self.uncorrected_round_mistakes) / len(
            self.uncorrected_round_mistakes
        )
        return AppBrain.calculate_score(
            total_chars=len(self.typed_chars),
            errors=average_error_count,
            test_time=MainFrame.ROUNDS_DURATION_MS,
        )


# TODO
# look into threading: there is lagging when user types quickly
