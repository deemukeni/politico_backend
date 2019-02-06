# write endpoints py
from flask import Flask, Blueprint, jsonify, request

from api.v1.models import Party

PARTIES = []

# use blueprint to version api endpoints
bp = Blueprint("apiv1", __name__, url_prefix="/api/v1")

@bp.route("/parties", methods=["POST"])
def create_party():
    """
    create a political party
    """
    data = request.get_json()
    try:
        name = data["name"]
        hqaddress = data["hqaddress"]
        logo_url = data["logo_url"]
    except KeyError:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    # does not accept empty fields
    if name == "" or hqaddress == "" or logo_url == "":
        resp = jsonify({"status": 400, "error": "All fields are required."})
        resp.status_code = 400
        return resp
    # name party has to be unique
    if Party.get_party_by_name(name):
        # a party with a similar name exists
        resp = jsonify({"status": 409, "error": "A party with a similar name exists"})
        resp.status_code = 409
        return resp
    # party object
    party = Party(name=name, hqaddress=hqaddress, logo_url=logo_url)
    # create party
    party.create_party()
    # convert party object to dictionary that is readily converted to json
    jsonify_party = party.to_json()
    resp = jsonify({"status": 201, "data": jsonify_party, "message": "Party created successfully."})
    resp.status_code = 201
    return resp

@bp.route("/parties", methods=["GET"])
def get_parties():
    parties = Party.get_all_parties()
    if len(parties) == 0:
        # no parties were found
        resp = jsonify({"status": 404, "data": parties, "message": "There are no parties."})
        resp.status_code = 404
        return resp
    else:
        resp = jsonify({"status": 200, "data": parties, "message": "Parties fetched successfully."})
        resp.status_code = 200
        return resp

@bp.route("/parties/<int:id>", methods=["GET"])
def get_single_party(id):
    party = Party.get_party_by_id(id)
    if party:
        # if party is found
        resp = jsonify({"status": 200, "data": party.to_json(), "message": "Party fetched successfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "data": party, "message": "Party not found."})
        resp.status_code = 200
        return resp

@bp.route("/parties/<int:id>", methods=["DELETE"])
def delete_party(id):
    party = Party.get_party_by_id(id)
    if party:
        # delete retrieved party
        Party.delete_party(id)
        resp = jsonify({"status": 200, "message": "Party deleted sucessfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "message": "Delete failed. Party not found."})
        resp.status_code = 404
        return resp
@bp.route("/offices" methods=["POST"])
def create_office():
    """
    Create an office
   
    """
    data = request.get_json
    try:
        id = data["id"]
        officetype = data["officetype"]
        name = data["name"]
    except KeyError:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    # does not accept empty fields
    if officetype == "" or name == "":
        resp = jsonify({"status": 400, "error": "All fields are required."})
        resp.status_code = 400
        return resp
    # office name has to be unique
    if Office.get_office_by_name(name):
        # a party with a similar name exists
        resp = jsonify({"status": 409, "error": "An ofice with a similar name exists"})
        resp.status_code = 409
        return resp
    # office object
    office = Office(name=name, officetype=officetype)
    # create office
    office.create_office()
    # convert office object to dictionary that is readily converted to json
    jsonify_office = office.to_json()
    resp = jsonify({"status": 201, "data": jsonify_office, "message": "Office created successfully."})
    resp.status_code = 201
    return resp

@bp.route("/offices" methods=["GET"])
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
