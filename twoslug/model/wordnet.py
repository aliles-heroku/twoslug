from __future__ import absolute_import
from functools import partial
import os
import random

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

def get_word(category, filter_fn=None, chooser=random):
    words = getattr(g, '_' + category, None)
    if words is None:
        words = tuple(sorted(load_words(category)))
        setattr(g, '_' + category, words)
    return chooser.choice(filter(filter_fn, words))

get_verb = partial(get_word, 'verb')
get_noun = partial(get_word, 'noun')
get_adjective = partial(get_word, 'adj')
get_adverb = partial(get_word, 'adv')
