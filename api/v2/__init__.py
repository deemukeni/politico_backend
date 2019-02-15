# create app factory, Blueprint
import os
from flask import Flask, Blueprint

from config import app_configurations
from api.v2.views.office_views import bp as offices
from api.v2.views.party_views import bp as parties
from api.v2.views.user_views import bp as users
from  api.v2.models.database import initiate_database, drop_tables


def create_app(environment):
    # create flask instance
    app = Flask(__name__)
    # get application configurations from config.py file
    app.config.from_object(app_configurations[environment])
    if environment == "testing":
        initiate_database(os.getenv("DATABASE_TEST_URL"))
    elif environment == "development":
        initiate_database(os.getenv("DATABASE_URL"))
    
    app.register_blueprint(offices)
    app.register_blueprint(parties)
    app.register_blueprint(users)

    return app
