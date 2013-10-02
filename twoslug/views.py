import calendar
import datetime
import random

from flask import abort, jsonify, render_template, request, url_for
from werkzeug.contrib.atom import AtomFeed

from twoslug import app
from twoslug import wordnet
from twoslug import duckduckgo

def page(verb, noun):
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


@app.route('/')
def index():
    verb = random.choice(wordnet.get_verbs())
    noun = random.choice(wordnet.get_nouns())
    return page(verb, noun)

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

@app.route('/feeds/atom.xml')
def atom():
    now = datetime.datetime.utcnow()
    today = datetime.datetime(now.year, now.month, now.day, 12 * (now.hour // 12))
    link = url_for('slugline', year=today.year, month=today.month,
            day=today.day, hour=today.hour, _external=True)
    seed = calendar.timegm(today.timetuple())
    chooser = random.Random(seed)
    verb = chooser.choice(wordnet.get_verbs()).capitalize()
    noun = chooser.choice(wordnet.get_nouns()).capitalize()
    slugline = '{0} {1}'.format(verb, noun)
    feed = AtomFeed('TwoSlug Today', feed_url=request.url, url=request.url_root)
    feed.add(title=slugline, title_type='text',
            content=slugline, content_type='text',
            published=today, updated=today,
            id=link, url=link,
            author='TwoSlug')
    return feed.get_response()

@app.route('/slugline/<int:year>/<int:month>/<int:day>/<int:hour>')
def slugline(year, month, day, hour):
    today = datetime.datetime(year, month, day, hour)
    seed = calendar.timegm(today.timetuple())
    chooser = random.Random(seed)
    verb = chooser.choice(wordnet.get_verbs())
    noun = chooser.choice(wordnet.get_nouns())
    return page(verb, noun)
