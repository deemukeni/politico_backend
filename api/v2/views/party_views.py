# write endpoints py
from flask import Flask, Blueprint, jsonify, request

from api.v2.models.models import Party
from api.v2.utils import helpers
from api.v2.views import bp
from api.v2.utils.helpers import token_required

# a list of all the parties where, after they are created, they are stored.
PARTIES = []



@bp.route("/parties", methods=["POST"])
@token_required
def create_party(user):
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
    # does not accept empty fields. if the users request is empty
    if helpers.required_fields(data, ["name", "hqaddress", "logo_url"]):
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
@token_required
def get_parties(user):
    parties = Party.get_all_parties()
    if len(parties) == 0:
        # no parties were found
        resp = jsonify({"status": 404, "data": parties, "error": "There are no parties."})
        resp.status_code = 404
        return resp
    else:
        resp = jsonify({"status": 200, "data": parties, "message": "Parties fetched successfully."})
        resp.status_code = 200
        return resp

@bp.route("/parties/<int:id>", methods=["GET"])
@token_required
def get_single_party(user, id):
    party = Party.get_party_by_id(id)
    if party:
        # if party is found
        resp = jsonify({"status": 200, "data": party.to_json(), "message": "Party fetched successfully."})
        resp.status_code = 200
        return resp
        # if party isn't found
    else:
        resp = jsonify({"status": 404, "data": party, "message": "Party not found."})
        resp.status_code = 404
        return resp

@bp.route("/parties/<int:id>", methods=["DELETE"])
@token_required
def delete_party(user, id):
    party = Party.get_party_by_id(id)
    if party:
        # after the getting the specific party by its id, delete retrieved party
        Party.delete_party(id)
        resp = jsonify({"status": 200, "message": "Party deleted sucessfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "message": "Delete failed. Party not found."})
        resp.status_code = 404
        return resp

