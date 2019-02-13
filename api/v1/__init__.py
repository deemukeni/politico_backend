# create app factory, Blueprint
from flask import Flask, Blueprint

from config import app_configurations
from api.v1.views import bp


def create_app(environment):
    # create flask instance
    app = Flask(__name__)
    # get application configurations from config.py file
    app.config.from_object(app_configurations[environment])
    
    app.register_blueprint(bp)

    return app