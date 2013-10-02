from functools import partial
import os

from flask import g

from twoslug import app


def load_words(category):
    words = set()
    filename = os.path.join(app.config['WORDNET'], 'index.' + category)
    with open(filename) as data:
        for line in data:
            word = line.split(None, 1)[0]
            if not word.isalpha():
                continue
            words.add(word)
    return words

def get_words(category):
    words = getattr(g, '_' + category, None)
    if words is None:
        words = tuple(sorted(load_words(category)))
        setattr(g, '_' + category, words)
    return words

get_verbs = partial(get_words, 'verb')
get_nouns = partial(get_words, 'noun')
get_adjectives = partial(get_words, 'adj')
get_adverbs = partial(get_words, 'adv')
