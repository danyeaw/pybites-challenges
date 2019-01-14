import itertools
import re

import pytest
from game import _validation
from game import draw_letters, calc_word_value, max_word_value
from game import get_possible_dict_words, _get_permutations_draw

NUM_LETTERS = 7
TEST_WORDS = ("bob", "julian", "pybites", "quit", "barbeque")


@pytest.fixture(scope="module")
def setup_game():
    return draw_letters()


def test_draw_letters(setup_game):
    letter_str = "".join(setup_game)
    assert re.search(r"^[A-Z]{%s}$" % NUM_LETTERS, letter_str)


# from ch01
def test_calc_word_value():
    assert calc_word_value("bob") == 7
    assert calc_word_value("JuliaN") == 13


# from ch01
def test_max_word_value():
    assert max_word_value(TEST_WORDS) == "barbeque"


@pytest.mark.xfail()
def test_get_permutations_draw(setup_game):
    draw = setup_game
    gen_permutations_n_letters = sum(
        len(list(itertools.permutations(draw, n))) for n in range(1, NUM_LETTERS + 1)
    )
    game_permutations = len(list(_get_permutations_draw(draw)))
    assert gen_permutations_n_letters == game_permutations
    alist = range(1, 8)
    gen_permutations_any_list = sum(
        len(list(itertools.permutations(alist, n))) for n in range(1, NUM_LETTERS + 1)
    )
    assert gen_permutations_any_list == gen_permutations_n_letters


@pytest.mark.xfail()
def test_get_possible_dict_words(setup_game):
    fixed_draw = list("garytev".upper())
    words = get_possible_dict_words(fixed_draw)
    assert len(words) == 137


def test_validation():
    draw = list("garytev".upper())
    # Test not in Dictionary
    word = "GARYTEV"
    with pytest.raises(ValueError):
        _validation(word, draw)
    # Test letter not in hand
    word = "F"
    with pytest.raises(ValueError):
        _validation(word, draw)
    # Test don't have 2 T's
    word = "GARETTA"
    with pytest.raises(ValueError):
        _validation(word, draw)
    # Test word is correct
    draw = list("Galanthus".upper())
    word = "Galanthus"
    assert _validation(word, draw)
    # Test don't have 3 a's
    word = "galanas"
    with pytest.raises(ValueError):
        _validation(word, draw)
