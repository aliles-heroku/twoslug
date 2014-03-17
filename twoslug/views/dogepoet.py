from __future__ import absolute_import
import calendar
import datetime
import random

from flask import abort, jsonify, redirect, render_template, request, url_for
from werkzeug.contrib.atom import AtomFeed

from twoslug import app
from twoslug.model import doge

def doge_page(first, second, last):
    poem = [
            ('verse', first),
            ('verse', second),
            ('finale', last)
    ]
    poetry = '{0}\n{1}\n{2}'.format(first, second, last)
    return render_template('dogepoet.html',
            brand='DogePoet',
            slug=poetry,
            title=poetry,
            poem=poem)

@app.route('/', subdomain='dogepoet')
def doge_index():
    mode = request.args.get('mode', None)
    if mode == 'alliteration':
      filter_fn = lambda item: item.startswith(verb[0])
    else:
      filter_fn = None
    first = doge.get_verse()
    second = doge.get_verse(filter_fn)
    last = doge.get_finale()
    return doge_page(first, second, last)

@app.route('/api/<path:path>/', subdomain='dogepoet')
def doge_api(path):
    poem = []
    mode = request.args.get('mode', None)
    filter_fn = None
    for element in path.split('/'):
        try:
            verse = {
                    'element': element,
                    'line': doge.get_doge(element, filter_fn)
            }
            poem.append(verse)
            if mode == 'alliteration' and filter_fn is None:
                filter_char = verse['line'].split()[-1][0]
                filter_fn = lambda item: item.startswith(filter_char)
        except ValueError:
            abort(400)
    return jsonify(poem=poem)

@app.route('/feeds/atom.xml', subdomain='dogepoet')
def doge_atom():
    now = datetime.datetime.utcnow()
    today = datetime.datetime(now.year, now.month, now.day, 12 * (now.hour // 12))
    seed = calendar.timegm(today.timetuple())
    link = url_for('doge_poem', seed=seed, _external=True)
    chooser = random.Random(seed)
    first = doge.get_verse(chooser=chooser)
    second = doge.get_verse(chooser=chooser)
    last = doge.get_finale(chooser=chooser)
    poetry = '{0}\n{1}\n{2}'.format(first, second, last)
    feed = AtomFeed('DogPoet Poetry', feed_url=request.url, url=request.url_root)
    feed.add(title=poetry, title_type='text',
            content=poetry, content_type='text',
            published=today, updated=today,
            id=link, url=link,
            author='DogePoet')
    return feed.get_response()

@app.route('/slugline/<int:seed>', subdomain='dogepoet')
def doge_poem(seed):
    chooser = random.Random(seed)
    first = doge.get_verse(chooser=chooser)
    second = doge.get_verse(chooser=chooser)
    last = doge.get_finale(chooser=chooser)
    return doge_page(first, second, last)

@app.route('/slugline/<int:year>/<int:month>/<int:day>/<int:hour>', subdomain='dogepoet')
def doge_date(year, month, day, hour):
    today = datetime.datetime(year, month, day, hour)
    seed = calendar.timegm(today.timetuple())
    return redirect(url_for('doge_poem', seed=seed))
