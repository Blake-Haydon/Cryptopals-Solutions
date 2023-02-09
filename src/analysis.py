import os
import json


def gen_letter_prob_arr():
    """Generates an array of letter probabilities. The index of the array
    is the ASCII value of the letter. The value of the array is the
    probability of the letter.
    """
    # Data taken from the following URL:
    # https://raw.githubusercontent.com/piersy/ascii-char-frequency-english/main/ascii_freq.json
    current_dir = os.path.dirname(__file__)
    ascii_freq_filepath = os.path.join(current_dir, "data/ascii_freq.json")

    # Load JSON
    with open(ascii_freq_filepath, "r") as f:
        ascii_freq = json.load(f)

    # Generate array
    letter_prob_arr = 256 * [0]
    for ascii_char in ascii_freq:
        letter_prob_arr[ascii_char["Char"]] = ascii_char["Freq"]

    return letter_prob_arr


def score_string(string: str) -> float:
    """Scores a string based on the letter probabilities of the English
    language. The score is the sum of the probabilities of each letter
    in the string.
    """
    letter_prob_arr = gen_letter_prob_arr()
    score = 0
    for char in string:
        score += letter_prob_arr[ord(char)]

    return score
