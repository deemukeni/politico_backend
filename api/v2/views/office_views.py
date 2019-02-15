# write endpoints py
from flask import Flask, Blueprint, jsonify, request

from api.v2.models.models import Office
from api.v2.utils import helpers
from api.v2.views import bp
from api.v2.utils.helpers import token_required
# a list of all the parties where, after they are created, they are stored.
PARTIES = []



@bp.route("/offices", methods=["POST"])
@token_required
def create_office(user):
    """
    Create an office

    """
    data = request.get_json()
    try:
        office_type = data["office_type"]
        office_name = data["office_name"]
    except KeyError:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    # does not accept empty fields
    if helpers.required_fields(data, ["office_type", "office_name"]):
        resp = jsonify({"status": 400, "error": "All fields are required."})
        resp.status_code = 400
        return resp
    helpers.check_whitespace(data)
    helpers.validate_names(data)
    # office name has to be unique
    row = Office.get_office_by_name(office_name)
    if row:        # a party with a similar name exists
        resp = jsonify({"status": 409, "error": "An office with a similar name exists"})
        resp.status_code = 409
        return resp
    # office object
    office = Office(name=office_name, office_type=office_type)
    # create office
    office.create_office()
    # convert office object to dictionary that is readily converted to json
    jsonify_office = {
        "office_type": office_type,
        "office_name": office_name
    }
    resp = jsonify({"status": 201, "data": jsonify_office, "message": "Office created successfully."})
    resp.status_code = 201
    return resp

@bp.route("/offices", methods=["GET"])
@token_required
def get_all_offices(user):
    offices = Office.get_all_offices()
    if len(offices) == 0:
        # no offices were found
        resp = jsonify({"status": 404, "data": offices, "message": "There are no offices."})
        resp.status_code = 404
        return resp
    else:
        resp = jsonify({"status": 200, "data": offices, "message": "Offices fetched successfully."})
        resp.status_code = 200
        return resp

@bp.route("/offices/<int:id>", methods=["GET"])
@token_required
def get_single_office(user, id):
    office = Office.get_office_by_id(id)
    if office:
        # if office is found
        resp = jsonify({"status": 200, "data": office, "message": "Office fetched successfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "data": office, "error": "Office not found."})
        resp.status_code = 404
        return resp

# @bp.route("/offices/<int:id>", methods=(["DELETE"]))
# @token_required
# def delete_office(user, id):
#     office = Office.get_office_by_id(id)
#     if office:
#         # delete retrieved office
#         Office.delete_office(id)
#         resp = jsonify({"status": 200, "message": "Office deleted sucessfully."})
#         resp.status_code = 200
#         return resp
#     else:
#         resp = jsonify({"status": 404, "message": "Delete failed. Office not found."})
#         resp.status_code = 404
#         return resp
