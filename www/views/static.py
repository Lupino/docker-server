import os
from www import app, static_file

@app.route('/static/:path#(.*)#')
def server_static(path):
    return static_file(path,  root = os.path.join(os.path.dirname(__file__), '../static'))

@app.route('/favicon.ico')
def server_favicon():
    return static_file('favicon.ico',  root = os.path.join(os.path.dirname(__file__), '../static'))
