from __future__ import absolute_import
import calendar
import datetime
import random

from flask import abort, jsonify, redirect, render_template, request, url_for
from werkzeug.contrib.atom import AtomFeed

from twoslug import app
from twoslug.model import markov

def get_length(request, default=8):
    try:
        return int(request.args.get('length', default))
    except ValueError:
        abort(400)

def wordinator_page(wordoid):
    return render_template('wordinator.html',
            brand='Wordinator',
            title=wordoid,
            wordoid=wordoid)

@app.route('/', subdomain='wordinator')
def wordinator_index():
    length = get_length(request, random.randint(5,10))
    wordoid = markov.generate_noun(length)
    return wordinator_page(wordoid)

@app.route('/api/<path:path>/', subdomain='wordinator')
def wordinator_api(path):
    wordoids = []
    length = get_length(request, random.randint(5,10))
    for category in path.split('/'):
        try:
            wordoids.append({
                    'class': category,
                    'wordoid': markov.generate_word(category, length)
            })
        except ValueError:
            abort(400)
    return jsonify(wordoids=wordoids)

@app.route('/feeds/atom.xml', subdomain='wordinator')
def wordinator_atom():
    now = datetime.datetime.utcnow()
    today = datetime.datetime(now.year, now.month, now.day, 12 * (now.hour // 12) + 6)
    seed = calendar.timegm(today.timetuple())
    link = url_for('wordinator_wordoid', seed=seed, _external=True)
    chooser = random.Random(seed)
    length = get_length(request, chooser.randint(5,10))
    wordoid = markov.generate_noun(length, chooser=chooser)
    feed = AtomFeed('Wordinator', feed_url=request.url, url=request.url_root)
    feed.add(title=wordoid, title_type='text',
            content=wordoid, content_type='text',
            published=today, updated=today,
            id=link, url=link,
            author='Wordinator')
    return feed.get_response()

@app.route('/wordoid/<int:seed>', subdomain='wordinator')
def wordinator_wordoid(seed):
    chooser = random.Random(seed)
    length = get_length(request, chooser.randint(5,10))
    wordoid = markov.generate_noun(length, chooser=chooser)
    return wordinator_page(wordoid)

@app.route('/wordoid/<int:year>/<int:month>/<int:day>/<int:hour>', subdomain='wordinator')
def wordinator_date(year, month, day, hour):
    today = datetime.datetime(year, month, day, hour)
    seed = calendar.timegm(today.timetuple())
    return redirect(url_for('wordinator_wordoid', seed=seed))
