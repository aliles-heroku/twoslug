from __future__ import absolute_import
from collections import Counter, defaultdict, namedtuple
from functools import partial
import bisect
import itertools
import os
import random

from flask import g

from twoslug import app

Node = namedtuple('Node', 'choices cumdist')

def populate_model(category, length):
    measures = defaultdict(Counter)
    filename = os.path.join(app.config['WORDNET'], 'index.' + category)
    with open(filename) as data:
        for line in data:
            word = line.split(None, 1)[0]
            if not word.isalpha():
                continue
            key = (None,) * length
            for letter in word:
                measures[key][letter] += 1
                key = key[1:] + (letter,)
    markov = {}
    for sequence in measures:
        choices, weights = zip(*sorted(measures[sequence].iteritems(),
            key=lambda n: n[1],
            reverse=True))
        cumdist = [0]
        for weight in weights:
            cumdist.append(cumdist[-1] + weight)
        markov[sequence] = Node(choices, cumdist[1:])
    return markov

def generate_word(category, length, chain_length=3, chooser=random):
    markov = getattr(g, '_%s_%d' % (category, chain_length), None)
    if markov is None:
        markov = populate_model(category, chain_length)
        setattr(g, '_%s_%d' % (category, chain_length), markov)
    key = (None,) * chain_length
    letters = []
    while len(letters) < length and key in markov:
        choices, cumdist = markov[key]
        choice = chooser.random() * cumdist[-1]
        letter = choices[bisect.bisect(cumdist, choice)]
        letters.append(letter)
        key = tuple(key + (letter,))[1:]
    return ''.join(letters)

generate_verb = partial(generate_word, 'verb')
generate_noun = partial(generate_word, 'noun')
generate_adjective = partial(generate_word, 'adj')
generate_adverb = partial(generate_word, 'adv')
