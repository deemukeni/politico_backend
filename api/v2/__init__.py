# create app factory, Blueprint
import os
from flask import Flask, Blueprint, jsonify

from config import app_configurations
from api.v2.views.office_views import bp as offices
from api.v2.views.party_views import bp as parties
from api.v2.views.user_views import bp as users
from api.v2.views.votes_views import bp as votes
from config import app_configurations

from  api.v2.models.database import initiate_database, drop_tables, QueryDatabase




def create_app(environment):
    # create flask instance
    app = Flask(__name__)
    # get application configurations from config.py file
    app.config.from_object(app_configurations[environment])
    # if environment == "testing":
    #     initiate_database(os.getenv("DATABASE_TEST_URL"))
    # elif environment == "development":
    #     initiate_database(os.getenv("DATABASE_URL"))
    db_url = app_configurations[environment].DATABASE_URL
    initiate_database(db_url)
    print("\n\n\n" ,db_url)

    if environment == "testing":
        drop_tables(db_url)
    QueryDatabase(db_url)
     
    app.register_blueprint(offices)
    app.register_blueprint(parties)
    app.register_blueprint(users)
    app.register_blueprint(votes)
    
    # error handlers
    @app.errorhandler(405)
    def method_not_allowed(err):
        return jsonify({"error": "method not allowed", "status": 405}), 405

    @app.errorhandler(404)
    def page_not_found(err):
        return jsonify({"error": "Page not found", "status": 404}), 404

    @app.errorhandler(500)
    def internal_server_error(err):
        return jsonify({"error": "Internal Server error", "status": 500}), 500

    return app
