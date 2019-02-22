import re
import os
import jwt
from functools import wraps

from flask import abort, make_response, jsonify, request

from api.v2.models.models import User

KEY = os.getenv('SECRET_KEY')


def required_fields(data, fields):
    """
    Checks if payload includes all the required data
    :return: None, if there are no empty fields
    """
    for field in fields:
        if data[field] == "":
            abort(make_response(
                jsonify({"error": "{} is required".format(field), "status": 400}), 400))


def validate_email(email):
    """
    checks if email format is correct
    :param email: user's emaill
    """
    if not re.match("^([a-zA-Z0-9_\-]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email):
        abort(make_response(jsonify({"error": "invalid email address"}), 400))


def validate_password(password):
    """
    checks if password is strong
    :param password: user's password
    """
    if not re.match("^[a-zA-Z]\w{3,14}$", password):
        abort(make_response(jsonify({"error": "invalid  password"})))

    if len(password) + 1 > 6:
        abort(make_response(jsonify({"error": "Password is too long"})))


def validate_names(data):
    """
    checks if name format is correct
    :param name: user's namel
    """
    for key, value in data.items():
        if key in ["first_name", "last_name", "other_name"]:
            if not value.isalpha():
                abort(make_response(
                    jsonify({"error": "Use letters in {}".format(key)})))


def validate_phone_number(phone_number):
    """
    Checks if the phone number is of the required length and is not a letter
    :param phone_number: user's phone number
    """
    if len(phone_number) + 1 > 10 and len(phone_number) + 1 < 10:
        a = abort(make_response(
            jsonify({"error": "Phone number entered is too long"})))
    if re.match("^[2-9]\d{2}-\d{3}-\d{4}$", phone_number):
        abort(make_response(jsonify({"error": "invalid phone number format"})))


def validate_office(office_type):
    """
    """
    office_types = ["federal", "legislative", "state", "local_governament"]
    if office_type not in office_types:
        return False


def token_required(f):
    """
    Creates a function to generate a token to  be used by the user as an authorization to carry out tasks
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "token_Bearer" in request.headers:
            token = request.headers['token_Bearer']
        if not token:
            abort(make_response(jsonify(
                {'error': 'You are not authorized to perform this action', "status": 401}), 401))

        user = None

        try:
            data = jwt.decode(token, KEY, algorithms="HS256")
            user = data['username']
            username = User.get_user_by_username(user)
        except:
            abort(make_response(
                jsonify({'error': "token is invalid", "status": 401}), 401))

        return f(user, *args, **kwargs)
    return decorated


def decode_token():
    token = request.headers['token_Bearer']
    data = jwt.decode(token, KEY)
    username = data['username']
    return username

def validate_image_url(image_url):
    if re.match(r"(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)", image_url):
        return True
    # return false if image url is invalid
    return False
