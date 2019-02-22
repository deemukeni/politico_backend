# write endpoints py
import datetime
import os
import json


from flask import Flask, jsonify, request, abort, make_response
import jwt

from api.v2.models.models import User
from api.v2.utils import helpers
from api.v2.views import bp

KEY = os.getenv("SECRET_KEY")

# User endpoints
@bp.route("/auth/sign-up", methods=(["POST"]))
def create_user():
    """
    A method to create a user.
    :param first_name: A string, the first_name name.
    :param last_name: A string, the last_name name.
    :param username: A string, the username name.
    :param phone_number: An integer, the user's phone number.
    :param email: A Varchar, the user's email.
    :param passport_url: A varchar, the users passport.
    :param password: A varchar, the user's password.
    :param confirm-password: A varchar, the user has confirm the password they  gave before
    :return: user created successfully.
    """
    data = request.get_json()
    try:
        first_name = data["first_name"].strip()
        last_name = data["last_name"].strip()
        username = data["username"].strip()
        email = data["email"].strip()
        phone_number = data["phone_number"].strip()
        passport_url = data["passport_url"].strip()
        password = data["password"].strip()
        role = data["role"].strip()
        confirm_password = data["confirm_password"].strip()

    except KeyError:
        # enforce use of appropriate keys (tells user to enter the appropriate keys since the ones entered were wrong)
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})#the actuall error to be shown to the user
        resp.status_code = 400
        return resp
    # does not accept empty fields. if the users request is empty
    helpers.required_fields(data, ["first_name", "last_name", "username", "email", "phone_number", "passport_url", "role"])

    helpers.validate_names(data)
    helpers.validate_email(email)
    print("GOT HERE")
    if len(phone_number) != 10:
        resp = jsonify({"status": 400, "error": "Phone number should be 10 characters long."})
        resp.status_code = 400
        return resp
    if not helpers.validate_image_url(passport_url):
        resp = jsonify({"status": 400, "error": "Invalid image url"})
        resp.status_code = 400
        return resp

    if password != confirm_password:
        resp = jsonify({"status": 400, "error": "Passwords do not match."})
        resp.status_code = 400
        return resp
    
    if len(password) < 6 or len(password) > 16:
        resp = jsonify({"error": "Password should be greater than 6 and less than 16 characters.", "status": 400})
        resp.status_code = 400
        return resp
    row = User.get_user_by_username(username)
    if row:
        resp = jsonify({"status": 400, "error": "A user with a similar username exists"})
        resp.status_code = 400
        return resp

    # a user with a similar phone number exists
    row = User.get_user_by_email(email)
    if row:
        resp = jsonify({"status": 400, "error": "A user with a similar email exists"})
        resp.status_code = 400
        return resp
    #user phone number has to be uique
    if User.get_user_by_phone_number(phone_number):
        # a user with a similar phone number exists
        resp = jsonify({"status": 400, "error": "A user with a similar phone number exists"})
        resp.status_code = 400
        return resp
    
    # user object
    user = User(first_name = first_name, last_name = last_name, username = username,
        email = email, phone_number = phone_number, passport_url = passport_url, password = password, role=role)
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
        "role": role,
        "confirm_password": confirm_password
    }
    resp = jsonify({"status": 201, "data": jsonify_user, "message": "User created successfully."})
    resp.status_code = 201
    return resp


@bp.route("/auth/signin", methods=['POST'])
def user_login():
    """
    A method to create a user.
    :param username: A string, the username.
    :param password: A string, the last_name name.
    :return: login successfull.
    """
    try:
        data=request.get_json()
        username = data["username"].strip()
        password = data["password"].strip()
    except:
        abort(make_response(jsonify({"status": 400, 
        "error": "All fields required."}), 400))

    user = User.get_user_by_username_and_password(username, password)
    if not user:
        return jsonify({"status": 404,
        "error":"Invalid username/password combination."}), 404

    payload = {"username":username}
    token = jwt.encode(payload, KEY, algorithm='HS256')
    token = token.decode('utf-8' )
    return jsonify({"message":"Logged in successfully", "status":200, "token":token}), 200


@bp.route("/auth/resetpassword", methods=["POST"])
def reset_password():
    """
    Allows user to reset their password
    """
    try:
        data = request.get_json()
        email = data["email"]
    except KeyError:
        abort(helpers.response(400, "error", "Should be email"))

    # use helper function to validate the email
    helpers.validate_email(email)
    # if user doesn't exist dont send an email to them
    try:
        user = UserModel.get_user_by_mail(email)
        if not user:
            abort(helpers.response(404, "error",
                                    "User does not exist. Create an account first"))
        return utils.response_fn(200, "data", [{
            "message": "Check your email for password reset link",
            "email": email
        }])
    except psycopg2.DatabaseError as _error:
        abort(helpers.response_fn(500, "error", "Server error"))
