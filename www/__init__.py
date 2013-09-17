import os
from .bottle import Bottle, TEMPLATE_PATH, static_file, request, response,\
    template, redirect

TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), './templates'))

app = Bottle()

from . import views

server = app
