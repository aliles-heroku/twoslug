import calendar
import datetime
import random

from flask import abort, jsonify, redirect, render_template, request, url_for
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
    mode = request.args.get('mode', None)
    if mode == 'alliteration':
      filter_fn = lambda item: item.startswith(verb[0])
    else:
      filter_fn = None
    noun = random.choice(filter(filter_fn, wordnet.get_nouns()))
    return page(verb, noun)

@app.route('/api/<path:path>/')
def api(path):
    words = []
    mode = request.args.get('mode', None)
    filter_fn = None
    for category in path.split('/'):
        try:
            word = {
                    'class': category,
                    'word': random.choice(filter(filter_fn, wordnet.get_words(category)))
            }
            if mode == 'alliteration' and filter_fn is None:
                filter_char = word['word'][0]
                filter_fn = lambda item: item.startswith(filter_char)
            words.append(word)
        except IOError:
            abort(400)
    return jsonify(slugline=words)

@app.route('/feeds/atom.xml')
def atom():
    now = datetime.datetime.utcnow()
    today = datetime.datetime(now.year, now.month, now.day, 12 * (now.hour // 12))
    seed = calendar.timegm(today.timetuple())
    link = url_for('slugline', seed=seed, _external=True)
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

@app.route('/slugline/<int:seed>')
def slugline(seed):
    chooser = random.Random(seed)
    verb = chooser.choice(wordnet.get_verbs())
    noun = chooser.choice(wordnet.get_nouns())
    return page(verb, noun)

@app.route('/slugline/<int:year>/<int:month>/<int:day>/<int:hour>')
def date(year, month, day, hour):
    today = datetime.datetime(year, month, day, hour)
    seed = calendar.timegm(today.timetuple())
    return redirect(url_for('slugline', seed=seed))
