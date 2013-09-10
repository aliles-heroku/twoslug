import random

from flask import abort, jsonify, render_template

from twoslug import app
from twoslug import wordnet
from twoslug import duckduckgo


@app.route('/')
def index():
    verb = random.choice(wordnet.get_verbs())
    noun = random.choice(wordnet.get_nouns())
    words = [
            ('verb', verb, duckduckgo.define(verb)),
            ('noun', noun, duckduckgo.define(noun))
    ]
    slugline = '{0} {1}'.format(verb, noun)
    return render_template('index.html',
            brand='TwoSlug',
            slug=slugline,
            title=slugline,
            words=words)

@app.route('/api/<path:path>/')
def api(path):
    words = []
    for category in path.split('/'):
        try:
            word = {
                    'class': category,
                    'word': random.choice(wordnet.get_words(category))
            }
            words.append(word)
        except IOError:
            abort(400)
    return jsonify(slugline=words)
