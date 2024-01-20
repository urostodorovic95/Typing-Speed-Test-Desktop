class AppBrain:
    def __init__(self, computer_text: str = None, user_text: str = None):
        self.computer_text = computer_text
        self.user_text = user_text
        if self.user_text:
            self._last_index = len(self.user_text) - 1

    @property
    def last_index(self):
        return self._last_index

    def is_last_char_same(self):
        return self.computer_text[self._last_index] == self.user_text[-1]

    def is_round_over(self):
        return len(self.computer_text.strip()) == len(self.user_text.strip())
