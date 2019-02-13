# write endpoints py
from flask import Flask, Blueprint, jsonify, request

from api.v2.models.models import User
from api.v2.utils import helpers

# a list of all the parties where, after they are created, they are stored.
PARTIES = []
# use blueprint to version api endpoints
bp = Blueprint("apiv2", __name__, url_prefix="/api/v2")
# for versioning : evry route will have /api/v1 prefixon it

# User endpoints
@bp.route("/users", methods=(["POST"]))
def create_user():
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        other_name = data["other_name"]
        email = data["email"]
        phone_number = data["phone_number"]
        passport_url = ["passport_url"]

    except KeyError:
        # enforce use of appropriate keys (tells user to enter the appropriate keys since the ones entered were wrong)
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})#the actuall error to be shown to the user
        resp.status_code = 400
        return resp
    # does not accept empty fields. if the users request is empty
    if helpers.required_fields(data, ["first_name", "last_name", "other_name", "email", "phone_number", "passport_url"]):
        resp = jsonify({"status": 400, "error": "All fields are required."})
        resp.status_code = 400
        return resp

    helpers.check_whitespace(data)
    helpers.validate_names(data)
    helpers.validate_email(email)

    #user email has to be uique
    if User.get_user_by_email(email):
        # a user with a similar email exists
        resp = jsonify({"status": 409, "error": "A user with a similar email exists"})
        resp.status_code = 409
        return resp
    #user phone number has to be uique
    if User.get_user_by_phone_number(phone_number):
        # a user with a similar phone number exists
        resp = jsonify({"status": 409, "error": "A user with a similar phone number exists"})
        resp.status_code = 409
        return resp
    
    # user object
    user = User(first_name = first_name, last_name = last_name, other_name = other_name, email = email, phone_number = phone_number, passport_url = passport_url)
    # call function that creates user
    user.create_user()
    # convert user object to dictionary that is readily converted to json
    jsonify_user = user.to_json()
    resp = jsonify({"status": 201, "data": jsonify_user, "message": "User created successfully."})
    resp.status_code = 201
    return resp
