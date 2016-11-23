from flask import Flask
from flask_bootstrap import Bootstrap

def create_app():
    flask = Flask(__name__)
    flask.config['DEBUG'] = True

    flask.secret_key = 'development'

    from .main.views import main as main_blueprint
    flask.register_blueprint(main_blueprint)
    return flask
