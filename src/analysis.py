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
        ascii_freq_file = json.load(f)

    # Generate array of normalized letter probabilities
    letter_prob_arr = 256 * [0]
    for ascii_char in ascii_freq_file:
        letter_prob_arr[ascii_char["Char"]] = ascii_char["Freq"]

    return letter_prob_arr


def score_string(string: str) -> float:
    """Scores a string based on the letter probabilities of the English
    language. The score is the sum of the probabilities of each letter
    in the string.
    """
    # If the string is empty, return 0
    if len(string) == 0:
        return 0

    # Count the number of occurrences of each letter
    letter_counts = 256 * [0]
    for char in string:
        letter_counts[ord(char)] += 1

    # Normalize letter counts
    letter_counts = [count / len(string) for count in letter_counts]
    # print(gen_letter_prob_arr())
    # print(letter_counts)
    # Calculate score
    score = 0
    letter_prob_arr = gen_letter_prob_arr()

    for i in range(256):
        score += abs(letter_counts[i] - letter_prob_arr[i])

    # Take reciprocal of score as a lower score is better (now a higher score is better)
    return 1 / score


print(score_string("!@#$%^&*"))
print(score_string("e e e e "))
