class AppBrain:
    def __init__(self, computer_text: str = None, user_text: str = None):
        self.computer_text = computer_text
        self.user_text = user_text

    def is_last_char_same(self):
        last_index = len(self.user_text) - 1
        return self.computer_text[last_index] == self.user_text[-1]

    def is_round_over(self):
        return len(self.computer_text) == len(self.user_text.strip())
