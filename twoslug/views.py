import random

from flask import abort, jsonify, render_template

from twoslug import app
from twoslug import wordnet


@app.route('/')
def index():
    verb = random.choice(wordnet.get_verbs())
    noun = random.choice(wordnet.get_nouns())
    slug = '{0} {1}'.format(verb, noun)
    return render_template('index.html', slug=slug, title='TwoSlug')

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
