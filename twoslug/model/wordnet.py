from __future__ import absolute_import
from collections import defaultdict
from functools import partial
import os
import random

from flask import g

from twoslug import app

SYNSET_TYPE = {
    '1': 'noun',
    '2': 'verb',
    '3': 'adj',
    '4': 'adv',
    '5': 'adj',
}

LEX_FNO = {
    '00': None,
    '01': None,
    '02': None,
    '03': None,
    '04': 'noun.act',
    '05': 'noun.animal',
    '06': 'noun.artifact',
    '07': 'noun.attribute',
    '08': 'noun.body',
    '09': 'noun.cognition',
    '10': 'noun.communication',
    '11': 'noun.event',
    '12': 'noun.feeling',
    '13': 'noun.food',
    '14': 'noun.group',
    '15': 'noun.location',
    '16': 'noun.motive',
    '17': 'noun.object',
    '18': 'noun.person',
    '19': 'noun.phenomenon',
    '20': 'noun.plant',
    '21': 'noun.possession',
    '22': 'noun.process',
    '23': 'noun.quantity',
    '24': 'noun.relation',
    '25': 'noun.shape',
    '26': 'noun.state',
    '27': 'noun.substance',
    '28': 'noun.time',
    '29': 'verb.body',
    '30': 'verb.change',
    '31': 'verb.cognition',
    '32': 'verb.communication',
    '33': 'verb.competition',
    '34': 'verb.consumption',
    '35': 'verb.contact',
    '36': 'verb.creation',
    '37': 'verb.emotion',
    '38': 'verb.motion',
    '39': 'verb.perception',
    '40': 'verb.possession',
    '41': 'verb.social',
    '42': 'verb.stative',
    '43': 'verb.weather',
    '44': None,
}

def load_words(category):
    wordnet = defaultdict(set)
    filename = os.path.join(app.config['WORDNET'], 'index.sense')
    with open(filename) as data:
        for line in data:
            word, lex_sense = line.split('%', 1)
            ss_type, lex_fno, _, _, _ = lex_sense.split(':')
            if not word.isalpha():
                continue
            ss_type = SYNSET_TYPE[ss_type]
            wordnet[ss_type].add(word)
            lex_fno = LEX_FNO[lex_fno]
            if lex_fno is None:
                continue
            wordnet[lex_fno].add(word)
    for ss_type in wordnet:
        words = tuple(sorted(wordnet[ss_type]))
        setattr(g, '_' + ss_type, words)
    return getattr(g, '_' + category)

def get_word(category, filter_fn=None, chooser=random):
    words = getattr(g, '_' + category, None)
    if words is None:
        words = load_words(category)
    return chooser.choice(filter(filter_fn, words))

get_verb = partial(get_word, 'verb')
get_noun = partial(get_word, 'noun')
get_adjective = partial(get_word, 'adj')
get_adverb = partial(get_word, 'adv')
