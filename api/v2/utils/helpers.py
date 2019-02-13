import re
from flask import abort, make_response, jsonify

def required_fields(data, fields):
    """
    data is the payload from the user
    fields is a list of required fields
    """
    for field in fields:
        if data[field] == "":
            return "All fields required."
    return None


def check_whitespace(data):
        for key,values in data.items():
                if not values.strip():
                        abort(make_response(jsonify({"error" : "invalid input at {}" .format(key)})))

def validate_email(email):
        if not re.match("^([a-zA-Z0-9_\-]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$", email):
                abort(make_response(jsonify({"error" : "invalid email address"})))

def validate_password(password):
        if not re.match("^[a-zA-Z]\w{3,14}$", password):
                abort(make_response(jsonify({"error" : "invalid  password"})))

def validate_names(data):
        for key,value in data.items():
                if key in ["first_name", "last_name", "other_name"]:
                        if not value.isalpha():
                                abort(make_response(jsonify({"error" : "use letters in {}".format(key)})))