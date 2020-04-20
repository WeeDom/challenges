#!python3
# Code Challenge 02 - Word Values Part II - a simple game
# http://pybit.es/codechallenge02.html

from itertools import permutations
from random import sample
from collections import defaultdict

from data import DICTIONARY, LETTER_SCORES, POUCH

NUM_LETTERS = 7


def draw_letters():
    """Pick NUM_LETTERS letters randomly. Hint: use stdlib random"""
    return sample(POUCH, NUM_LETTERS)


draw = draw_letters()


def input_word(words):
    """Ask player for a word and validate against draw.
    Use _validation(word, draw) helper."""
    word = input("Form a valid word: ")
    if _validation(words, word):
        return word
    else:
        return False


def is_word_in_dictionary(words, word):
    return word.lower() in words


def _validation(words, word):
    """Validations: 1) only use letters of draw, 2) valid dictionary word"""
    # uc word
    # check word is ascii and letters only - no spaces
    num_letters_draw = defaultdict(int)
    num_letters_word = defaultdict(int)
    for char in draw:
        num_letters_draw[char] += 1

    for char in word:
        num_letters_word[char] += 1
    if word.isalpha():
        # split into individual chars
        for char in word:
            # check word only contains chars in draw
            if char.upper() not in draw:
                print("{} was not in the draw ({})".format(char, draw))
                return False
            if num_letters_word[char.upper()] > num_letters_draw[char.upper()]:
                print(
                    "{} occured {} times in the word, " +
                    "but there's only {} in the draw ({})"
                    .format(
                        char,
                        num_letters_word[char], num_letters_draw[char], draw))
                return False
    return is_word_in_dictionary(words, word)


def calc_word_value(word):
    """Calc a given word value based on Scrabble LETTER_SCORES mapping"""
    return sum(LETTER_SCORES.get(char.upper(), 0) for char in word)


def get_possible_dict_words(draw):
    """Get all possible words from draw which are valid dictionary words.
    Use the _get_permutations_draw helper and DICTIONARY constant"""
    words_in_rack = []
    perms = [''.join(p).lower() for p in _get_permutations_draw(draw)]
    words = load_words()
    words_in_rack = words.intersection(perms)

    return words_in_rack


def _get_permutations_draw(draw, r=None):
    """Helper for get_possible_dict_words to get all permutations of draw letters.
    Hint: use itertools.permutations"""
    for r in range(1, NUM_LETTERS):
        previous = tuple()
        for perm in permutations(sorted(draw), r):
            if perm > previous:
                previous = perm
                yield perm


def max_word_value(words):
    """Calc the max value of a collection of words"""
    return max(words, key=calc_word_value)


def load_words():
    """Load dictionary into a list and return list"""
    return DICTIONARY


def main():
    """Main game interface calling the previously defined methods"""
    print('Letters drawn: {}'.format(', '.join(draw)))
    words = load_words()
    word = input_word(words)
    word_score = 0
    if word is False:
        print("Not a valid word: {}".format(word))
    else:
        word_score = calc_word_value(word)
        print('Word chosen: {} (value: {})'.format(word, word_score))

    possible_words = get_possible_dict_words(draw)

    max_word = max_word_value(possible_words)
    max_word_score = calc_word_value(max_word)
    print('Optimal word possible: {} (value: {})'.format(
        max_word, max_word_score))

    game_score = word_score / max_word_score * 100
    print('You scored: {:.1f}%'.format(game_score))


if __name__ == "__main__":
    main()
