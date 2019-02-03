# create app factory
from flask import Flask

from config import app_configurations

def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(app_configurations[environment])

    return app
