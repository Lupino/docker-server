import os
import config
from .bottle import Bottle, TEMPLATE_PATH, static_file, request, response,\
    template, redirect

TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(__file__), './templates'))
from .server import TulipBottle
app = TulipBottle()
from . import bottle_login

login_plugin = bottle_login.Plugin()
app.install(login_plugin)

from . import views

from beaker.middleware import SessionMiddleware
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 7 * 24 * 60 * 60,
    'session.data_dir': 'run',
    'session.auto': True
}

server = SessionMiddleware(app, session_opts)
