import os
from flask import Flask


app = Flask(__name__)


def random_slug():
    return ''


@app.route('/')
def index():
    return random_slug()


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
