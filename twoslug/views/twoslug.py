from __future__ import absolute_import
import calendar
import datetime
import random

from flask import abort, jsonify, redirect, render_template, request, url_for
from werkzeug.contrib.atom import AtomFeed

from twoslug import app
from twoslug.model import wordnet
from twoslug.utils import duckduckgo, schedule

def get_chooser():
    chooser = random
    for param, base in (('oct', 8), ('seed', 10), ('int', 10), ('hex', 16), ('hash', 16)):
        value = request.args.get(param, None)
        if value is not None:
            chooser = random.Random(int(value, base))
    return chooser

def twoslug_page(verb, noun):
    words = [
            ('verb', verb, duckduckgo.define(verb)),
            ('noun', noun, duckduckgo.define(noun))
    ]
    slugline = '{0} {1}'.format(verb, noun)
    return render_template('twoslug.html',
            brand='TwoSlug',
            slug=slugline,
            title=slugline,
            words=words)

@app.route('/', subdomain='twoslug')
def twoslug_index():
    chooser = get_chooser()
    verb = wordnet.get_verb(chooser=chooser)
    mode = request.args.get('mode', None)
    if mode == 'alliteration':
      filter_fn = lambda item: item.startswith(verb[0])
    else:
      filter_fn = None
    noun = wordnet.get_noun(filter_fn, chooser=chooser)
    return twoslug_page(verb, noun)

@app.route('/api/<path:path>/', subdomain='twoslug')
def twoslug_api(path):
    words = []
    chooser = get_chooser()
    mode = request.args.get('mode', None)
    filter_fn = None
    for category in path.split('/'):
        try:
            word = {
                    'class': category,
                    'word': wordnet.get_word(category, filter_fn, chooser=chooser)
            }
            if mode == 'alliteration' and filter_fn is None:
                filter_char = word['word'][0]
                filter_fn = lambda item: item.startswith(filter_char)
            words.append(word)
        except IOError:
            abort(400)
    return jsonify(slugline=words)

@app.route('/feeds/atom.xml', subdomain='twoslug')
def twoslug_atom():
    released = schedule.regular()
    seed = calendar.timegm(released.timetuple())
    link = url_for('twoslug_slugline', seed=seed, _external=True)
    chooser = random.Random(seed)
    verb = wordnet.get_verb(chooser=chooser).capitalize()
    noun = wordnet.get_noun(chooser=chooser).capitalize()
    slugline = '{0} {1}'.format(verb, noun)
    feed = AtomFeed('TwoSlug Today', feed_url=request.url, url=request.url_root)
    feed.add(title=slugline, title_type='text',
            content=slugline, content_type='text',
            published=released, updated=released,
            id=link, url=link,
            author='TwoSlug')
    return feed.get_response()

@app.route('/slugline/hex/<hex:seed>', subdomain='twoslug')
@app.route('/slugline/int/<int:seed>', subdomain='twoslug')
@app.route('/slugline/oct/<oct:seed>', subdomain='twoslug')
@app.route('/slugline/<int:seed>', subdomain='twoslug')
def twoslug_slugline(seed):
    chooser = random.Random(seed)
    verb = wordnet.get_verb(chooser=chooser)
    noun = wordnet.get_noun(chooser=chooser)
    return twoslug_page(verb, noun)

@app.route('/slugline/<int:year>/<int:month>/<int:day>/<int:hour>', subdomain='twoslug')
def twoslug_date(year, month, day, hour):
    today = datetime.datetime(year, month, day, hour)
    seed = calendar.timegm(today.timetuple())
    return redirect(url_for('twoslug_slugline', seed=seed))
