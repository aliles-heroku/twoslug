from __future__ import absolute_import
from flask import Flask, render_template

def send_static_file(subdomain, filename):
    return app.send_static_file(filename)

app = Flask(__name__, static_folder=None)
app.config.from_object('config')
app.static_folder = 'static'
app.add_url_rule('/static/<path:filename>',
        endpoint='static', subdomain='<subdomain>',
        view_func=send_static_file)

from . import views
