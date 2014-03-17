from functools import partial
import random

from flask import g

from . import wordnet

VERSE = sorted(('many', 'much', 'so', 'such', 'very'))
FINALE = sorted(('amaze', 'excite', 'wow', 'wow', 'wow'))

def get_verse(filter_fn=None, chooser=random):
    words = getattr(g, '_doge', None)
    category = chooser.choice(('adj', 'noun', 'verb'))
    return " ".join((chooser.choice(VERSE),
        wordnet.get_word(category, filter_fn, chooser)))

def get_finale(chooser=random):
    return chooser.choice(FINALE)

def get_doge(element, filter_fn=None, chooser=random):
    if element == 'verse':
        return get_verse(filter_fn, chooser)
    elif element == 'finale':
        return get_finale(chooser)
    else:
        raise ValueError('Unknown doge element')
