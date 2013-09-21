from www import app, config, request, template

@app.route('/')
def index():
    return template('index', config = config)
