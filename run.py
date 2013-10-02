#!/usr/bin/env python
import begin
from twoslug import app

@begin.start
@begin.convert(port=int)
def main(host='127.0.0.1', port=8000, debug=False):
    app.run(host=host, port=port, debug=debug)
