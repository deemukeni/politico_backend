# write endpoints py
from flask import Flask, Blueprint, jsonify, request, abort, make_response

from api.v2.models.models import Office
from api.v2.utils import helpers
from api.v2.views import bp
from api.v2.utils.helpers import token_required


@bp.route("/offices", methods=["POST"])
@token_required
def create_office(user):
    """"
    A method to create an office.
    :param user: token
    """
    data = request.get_json()
    try:
        office_type = data["office_type"].strip()
        office_name = data["office_name"].strip()
    except KeyError:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    # does not accept empty fields
    helpers.required_fields(data, ["office_type", "office_name"])
    helpers.validate_names(data)
    # office name has to be unique
    row = Office.get_office_by_name(office_name)
    if row:        # a party with a similar name exists
        resp = jsonify({"status": 400, "error": "An office with a similar name exists"})
        resp.status_code = 400
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
    """
    Get all available offices
    """
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
    """
    Get a specific office by its id
    """

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

@bp.route("/offices/<int:id>", methods=(["DELETE"]))
@token_required
def delete_office(user, id):
    """
    Delete an office from the database
    """
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


@bp.route("/offices/<int:id>", methods=["PATCH"])
@token_required
def update_office(user, id):
    """
    
    """
    data = request.get_json()
    try:
        office_name = data['office_name']
        office_type = data['office_type']
    except:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    if not office_type or not office_name:
        abort(make_response(jsonify({"error" : "Cannot update with empty fields", "status" : 400}), 400))
    office = Office.get_office_by_id(id)
    if helpers.validate_office(office_type) == False:
        abort(make_response(jsonify({"error" : "Acceptable office types are federal, legislative, state, local_governament.", "status" : 404}), 404))

    if office:
        Office.update_office(office_name=office_name, office_type=office_type, office_id=id)
        # after the getting the specific office by its id, delete retrieved office
        resp = jsonify({"status": 200, "message": "office updated successfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "message": "Office not found."})
        resp.status_code = 404
        return resp
