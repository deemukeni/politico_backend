# write endpoints py
import datetime
import os
import json


from flask import Flask, jsonify, request, abort, make_response
import jwt

from api.v2.models.models import User
from api.v2.utils import helpers
from api.v2.views import bp
from api.v2.models.database import select_from_database

KEY = os.getenv("SECRET_KEY")

# User endpoints
@bp.route("/auth/sign-up", methods=(["POST"]))
def create_user():
    data = request.get_json()
    try:
        first_name = data["first_name"]
        last_name = data["last_name"]
        username = data["username"]
        email = data["email"]
        phone_number = data["phone_number"]
        passport_url = data["passport_url"]
        password = data["password"]
        confirm_password = data["confirm_password"]

    except KeyError:
        # enforce use of appropriate keys (tells user to enter the appropriate keys since the ones entered were wrong)
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})#the actuall error to be shown to the user
        resp.status_code = 400
        return resp
    helpers.check_whitespace(data)
    # does not accept empty fields. if the users request is empty
    if helpers.required_fields(data, ["first_name", "last_name", "username", "email", "phone_number", "passport_url"]):
        resp = jsonify({"status": 400, "error": "All fields are required."})
        resp.status_code = 400
        return resp

    helpers.check_whitespace(data)
    helpers.validate_names(data)
    helpers.validate_email(email)

    row = User.get_user_by_username(username)
    if row:
        resp = jsonify({"status": 409, "error": "A user with a similar username exists"})
        resp.status_code = 409
        return resp

    # a user with a similar phone number exists
    row = User.get_user_by_email(email)
    if row:
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
    user = User(first_name = first_name, last_name = last_name, username = username,
        email = email, phone_number = phone_number, passport_url = passport_url, password = password)
    # call function that creates user
    user.create_user()
    # convert user object to dictionary that is readily converted to json
    jsonify_user = {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "email": email,
        "phone_number": phone_number,
        "passport_url": passport_url,
        "password": password,
        "confirm_password": confirm_password
    }
    resp = jsonify({"status": 201, "data": jsonify_user, "message": "User created successfully."})
    resp.status_code = 201
    return resp


@bp.route("/auth/signin", methods=['POST'])
def user_login():
    """
    User can login
    """
    try:
        data=request.get_json()
        username = data["username"]
        password = data["password"]
    except:
        abort(make_response(jsonify({"status": 400, 
        "error": "Use uniform keys."}), 400))
        helpers.check_whitespace(data)

    user = User.get_user_by_username(username)
    if not user:
        return jsonify({"status": 404,
                        "error":"Invalid username/password combination."}), 404

    password = User.get_user_by_password(password)
    if not password:
        abort(make_response(jsonify({'status': 404,
                                        'error': "Invalid username/password combination."}), 404))

    payload = {"username":username, 'exp':datetime.datetime.utcnow()+ datetime.timedelta(hours=5)}

    token = jwt.encode(payload, KEY, algorithm='HS256')

    token = token.decode('utf-8')

    return jsonify({"message":"Logged in successfully", "status":200, "token":token}), 200
