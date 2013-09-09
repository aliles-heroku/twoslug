import random

from flask import render_template

from twoslug import app
from twoslug import wordnet


@app.route('/')
def index():
    verb = random.choice(wordnet.get_verbs())
    noun = random.choice(wordnet.get_nouns())
    return render_template('index.html', slug='{0} {1}'.format(verb, noun))
