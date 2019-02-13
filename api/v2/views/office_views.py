# write endpoints py
from flask import Flask, Blueprint, jsonify, request

from api.v2.models.models import Office
from api.v2.utils import helpers

# a list of all the parties where, after they are created, they are stored.
PARTIES = []
# use blueprint to version api endpoints
bp = Blueprint("apiv2", __name__, url_prefix="/api/v2")
# for versioning : evry route will have /api/v1 prefixon it


@bp.route("/offices", methods=["POST"])
def create_office():
    """
    Create an office

    """
    data = request.get_json()
    try:
        office_type = data["office_type"]
        name = data["name"]
    except KeyError:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    # does not accept empty fields
    if required_fields(data, ["office_type", "name"]):
        resp = jsonify({"status": 400, "error": "All fields are required."})
        resp.status_code = 400
        return resp
    # office name has to be unique
    if Office.get_office_by_name(name):
        # a party with a similar name exists
        resp = jsonify({"status": 409, "error": "An office with a similar name exists"})
        resp.status_code = 409
        return resp
    # office object
    office = Office(name=name, office_type=office_type)
    # create office
    office.create_office()
    # convert office object to dictionary that is readily converted to json
    jsonify_office = office.to_json()
    resp = jsonify({"status": 201, "data": jsonify_office, "message": "Office created successfully."})
    resp.status_code = 201
    return resp

@bp.route("/offices", methods=["GET"])
def get_all_offices():
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
def get_single_office(id):
    office = Office.get_office_by_id(id)
    if office:
        # if office is found
        resp = jsonify({"status": 200, "data": office.to_json(), "message": "Office fetched successfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "data": office, "error": "Office not found."})
        resp.status_code = 404
        return resp

@bp.route("/offices/<int:id>", methods=(["GET"]))
def delete_office(id):
    office = Office.get_office_by_id(id)
    if office:
        # delete retrieved office
        Office.delete_office(id)
        resp = jsonify({"status": 200, "message": "Office deleted sucessfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "message": "Delete failed. Office not found."})
        resp.status_code = 404
        return resp
