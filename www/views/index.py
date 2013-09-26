from www import app, config, template

@app.route('/')
def index():
    return template('index', config = config)
