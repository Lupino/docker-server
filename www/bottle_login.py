__author__ = "Li Meng Jun"
__version__ = '0.0.1'
__license__ = 'MIT'

### CUT HERE (see setup.py)

import inspect
from .bottle import request, redirect, PluginError


class LoginPlugin(object):
    '''
    '''
    name = 'login'

    def __init__(self, session_key='user', keyword='user'):
        self.keyword = keyword
        self.session_key = session_key
        self.app = None
        self.session = {}
    def setup(self, app):
        '''
        Make sure that other installed plugins don't affect the same keyword argument.
        '''
        self.app = app
        for other in app.plugins:
            if not isinstance(other, LoginPlugin):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another login plugin with conflicting settings (non-unique keyword).")
        self.app.hooks.add('before_request', self.load_session)
        self.app.hooks.add('after_request', self.set_session)
        self.app.login = self.login

    def load_session(self):
        self.session = request.environ.get('beaker.session', {})

    def set_session(self):
        pass

    def login(self, user):
        '''
        Store the login user to session.
        '''
        self.session[self.session_key] = user

    def apply(self, callback, context):
        conf = context['config'].get('login') or {}
        keyword = conf.get('keyword', self.keyword)
        session_key = conf.get('session_key', self.session_key)
        args = inspect.getargspec(context['callback'])[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[keyword] = self.session.get(session_key)
            if kwargs[keyword]:
                return callback(*args, **kwargs)
            return {'err': 'not permission'}

        # Replace the route callback with the wrapped one.
        return wrapper

Plugin = LoginPlugin
