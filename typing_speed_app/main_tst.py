import random


def generate_words(n: int = 5) -> list:
    """
    Generates a list of randomly selected words from a file.

    Parameters:
    - n (int, optional): The number of words to generate. Default is 5.

    Returns:
    - list: A list containing the randomly selected words.

    Example:
    >>> word_list = generate_words(3)
    >>> print(word_list)
    ['word1', 'word2', 'word3']
    """
    with open("typing_speed_app/words_bank.txt", encoding="UTF-8") as words_file:
        random_lines = random.sample(
            [line.strip() for line in words_file.readlines()], n
        )
        return random_lines

