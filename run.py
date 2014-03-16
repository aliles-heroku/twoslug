#!/usr/bin/env python
import begin
from twoslug import app

@begin.start
@begin.convert(port=int)
def main(host='local', port=8000, debug=False):
    app.config['SERVER_NAME'] = '%s:%d' % (host, port)
    app.run(host=host, port=port, debug=debug)
