class AppBrain:
    def __init__(self, computer_text: str = None, user_text: str = None):
        self.computer_text = computer_text
        self.user_text = user_text
        self.round_mistakes = 0
        self._last_index = len(self.user_text) - 1

    @staticmethod
    def calculate_score(total_chars: int, errors: int, test_time: int = 60000):
        return (
            int((total_chars / 5 - errors) / ((test_time / 1000) / 60)),
            int(errors),
        )

    @property
    def last_index(self):
        return self._last_index

    def is_last_char_same(self):
        if len(self.user_text) == 0:
            return False
        return self.computer_text[self._last_index] == self.user_text[-1]

    def is_round_over(self):
        return len(self.computer_text.strip()) == len(self.user_text.strip())

    @property
    def round_mistakes(self):
        return self._round_mistakes

    @round_mistakes.setter
    def round_mistakes(self, new_value):
        if new_value > len(self.computer_text):
            raise ValueError("More mistakes than letters!")
        self._round_mistakes = new_value

    def count_round_errors(self) -> int:
        errors = 0
        for index, char in enumerate(self.user_text.strip()):
            if char != self.computer_text.strip()[index]:
                errors += 1
        return errors
