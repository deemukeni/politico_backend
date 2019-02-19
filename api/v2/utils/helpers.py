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
            return "All fields required."
    return None


def check_whitespace(data):
        """
        Checks for any whitespacein the input data
        :param data: actual data
        """
        for key,values in data.items():
                if not values.strip():
                        abort(make_response(jsonify({"error" : "invalid input at {}" .format(key)}), 400))

def validate_email(email):
        """
        checks if email format is correct
        :param email: user's emaill
        """
        if not re.match("^([a-zA-Z0-9_\-]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email):
                abort(make_response(jsonify({"error" : "invalid email address"})))

def validate_password(password):
        """
        checks if password is strong
        :param password: user's password
        """
        if not re.match("^[a-zA-Z]\w{3,14}$", password):
                abort(make_response(jsonify({"error" : "invalid  password"})))

        if len(password) +1  > 6:
                abort(make_response(jsonify({"error" : "Password is too long"})))

def validate_names(data):
        """
        checks if name format is correct
        :param name: user's namel
        """
        for key,value in data.items():
                if key in ["first_name", "last_name", "other_name"]:
                        if not value.isalpha():
                                abort(make_response(jsonify({"error" : "use letters in {}".format(key)})))

def validate_phone_number(phone_number):
        """
        Checks if the phone number is of the required length
        :param phone_number: user's phone number
        """
        if len(phone_number) + 1 > 10:
                a = abort(make_response(jsonify({"error" : "Phone number entered is too long"})))
                

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
                        abort(make_response(jsonify({'error':'Token is missing', "status":401}), 401))

                user = None

                try:
                        data = jwt.decode(token, KEY, algorithms="HS256")
                        print(data)
                        user = data['username']
                        username = User.get_user_by_username(user)

                except:
                        abort(make_response(jsonify({'error':"token is invalid", "status":401}), 401))

                return f(user, *args, **kwargs)
        return decorated

def decode_token():
        token = request.headers['token_bearer']

        data = jwt.decode(token, KEY)

        username  = data['username']
        return username