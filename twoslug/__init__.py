from __future__ import absolute_import
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

from twoslug import views
