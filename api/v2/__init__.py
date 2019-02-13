# create app factory, Blueprint
from flask import Flask, Blueprint

from config import app_configurations
from api.v2.views import bp
from  api.v2.models.database import connect_db, create_tables, initiate_database


def create_app(environment):
    # create flask instance
    app = Flask(__name__)
    # get application configurations from config.py file
    app.config.from_object(app_configurations[environment])
    initiate_database()
    
    app.register_blueprint(bp)

    return app
