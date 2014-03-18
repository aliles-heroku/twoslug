from functools import partial
import random

from flask import g

from . import wordnet

VERSE = sorted(('many', 'much', 'so', 'such', 'very'))
FINALE = sorted(('amaze', 'excite', 'wow', 'wow', 'wow'))

def get_verse(filter_reference=None, filter_delimeter=None, chooser=random):
    words = getattr(g, '_doge', None)
    category = chooser.choice(('adj', 'noun', 'verb'))
    return (chooser.choice(filter(filter_delimeter, VERSE)),
        wordnet.get_word(category, filter_reference, chooser))

def get_finale(chooser=random):
    return (chooser.choice(FINALE),)

def get_doge(element, filter_reference=None, filter_delimeter=None, chooser=random):
    if element == 'verse':
        return get_verse(filter_reference, filter_delimeter, chooser)
    elif element == 'finale':
        return get_finale(chooser)
    else:
        raise ValueError('Unknown doge element')
