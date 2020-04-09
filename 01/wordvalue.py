from data import DICTIONARY, LETTER_SCORES
import errno
import os

def load_words():
    """Load dictionary into a list and return list"""
    try:
        with open(DICTIONARY) as f:
            words = [line.rstrip() for line in f]
            return words
    except:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), DICTIONARY)

def calc_word_value(word):
    """Calculate the value of the word entered into function
    using imported constant mapping LETTER_SCORES"""
    score = []
    for char in word:
        if char in ['-']:
            return 0
        else:
            score.append(LETTER_SCORES[char.upper()])

    return sum(score)
    pass

def max_word_value(words=load_words()):
    """Calculate the word with the max value, can receive a list
    of words as arg, if none provided uses default DICTIONARY"""
    winner_score = 0
    winner = ''
    for word in words:
       score = calc_word_value(word)
       if score > winner_score:
            winner = word
            winner_score = score

    return winner

if __name__ == "__main__":
    pass # run unittests to validate
