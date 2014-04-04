#!/usr/bin/env python
import begin
from twoslug import app, model

@begin.subcommand
@begin.convert(length=int, chain=int, words=int)
def markov(category='noun', length=10, chain=3, words=1):
    with app.app_context():
        for _ in xrange(words):
            print model.markov.generate_word(category, length, chain)

@begin.subcommand
@begin.convert(port=int)
def web(host='local', port=8000, debug=False):
    app.config['SERVER_NAME'] = '%s:%d' % (host, port)
    app.run(host=host, port=port, debug=debug)

@begin.start
def main():
    pass
