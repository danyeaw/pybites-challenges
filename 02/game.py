#!python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

import itertools
import random

from data import DICTIONARY, LETTER_SCORES, POUCH

NUM_LETTERS = 7


def draw_letters():
    """Pick NUM_LETTERS letters randomly. Hint: use stdlib random"""
    hand = []
    for draw in range(NUM_LETTERS):
        hand.append(POUCH[random.randrange(len(POUCH))])
    return hand


def input_word(draw):
    """Ask player for a word and validate against draw.
    Use _validation(word, draw) helper."""
    word = input("Enter the word you would like to play: ")
    if _validation(word, draw):
        return word
    else:
        input_word(word)


def _validation(word, draw):
    """Validations: 1) only use letters of draw, 2) valid dictionary word"""
    unused_chars = draw.copy()
    for char in list(word.upper()):
        if char in unused_chars:
            unused_chars.remove(char)
        else:
            raise ValueError(f"You don't have {char} in your hand")
    if word.lower() not in DICTIONARY:
        raise ValueError(f"The word {word} is not in the dictionary")
    return True


# From challenge 01:
def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


def get_possible_dict_words(draw):
    """Get all possible words from draw which are valid dictionary words.
    Use the _get_permutations_draw helper and DICTIONARY constant"""
    possible_words = []
    for word in _get_permutations_draw(draw):
        if "".join(word).lower() in DICTIONARY:
            possible_words.append(word)
    return possible_words


def _get_permutations_draw(draw):
    """Helper for get_possible_dict_words to get all permutations of draw letters.
    Hint: use itertools.permutations"""
    for r in range(1, NUM_LETTERS + 1):
        yield from list(itertools.permutations(draw, r))


# From challenge 01:
def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)


def main():
    """Main game interface calling the previously defined methods"""
    draw = draw_letters()
    print(f"Letters drawn: {draw}")

    word = input_word(draw)
    word_score = calc_word_value(word)
    print(f"Word chosen: {word} (value: {word_score})")

    possible_words = get_possible_dict_words(draw)

    max_word = max_word_value(possible_words)
    max_word_score = calc_word_value(max_word)
    print(f"Optimal word possible: {max_word} (value: {max_word_score})")

    game_score = word_score / max_word_score * 100
    print(f"You scored: {game_score:.1f}")


if __name__ == "__main__":
    main()
