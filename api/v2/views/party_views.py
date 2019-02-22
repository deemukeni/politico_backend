# write endpoints py
from flask import Flask, Blueprint, jsonify, request

from api.v2.models.models import Party
from api.v2.utils import helpers
from api.v2.views import bp
from api.v2.utils.helpers import token_required, validate_image_url

# a list of all the parties where, after they are created, they are stored.
PARTIES = []

@bp.route("/parties", methods=["POST"])
@token_required
def create_party(user):
    """
    A method to create a user.
    :param party_name: A string, the party name.
    :param party_logo: A string, the party logo.
    :return resp: json response
    """
    data = request.get_json()
    try:
        name = data["name"].strip()
        hqaddress = data["hqaddress"].strip()
        logo_url = data["logo_url"].strip()
    except KeyError:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    # does not accept empty fields. if the users request is empty
    helpers.required_fields(data, ["name", "hqaddress", "logo_url"])
        
    # name party has to be unique
    if Party.get_party_by_name(name):
        # a party with a similar name exists
        resp = jsonify({"status": 400, "error": "A party with a similar name exists"})
        resp.status_code = 400
        return resp

    row = Party.get_party_by_name(name)
    if row:
        resp = jsonify({"status": 400, "error": "A party with a similar name exists"})
        resp.status_code = 400
        return resp
    
    # validate logo url
    if not validate_image_url(logo_url):
        resp = jsonify({"status": 400, "error": "Invalid image url"})
        resp.status_code = 400
        return resp
    # party object
    party = Party(name=name, hqaddress=hqaddress, logo_url=logo_url)
    # create party
    party.create_party()
    # convert party object to dictionary that is readily converted to json
    jsonify_party = {
        "name" : name,
        "hqaddress" : hqaddress,
        "logo_url" : logo_url
    }
    resp = jsonify({"status": 201, "data": jsonify_party, "message": "Party created successfully."})
    resp.status_code = 201
    return resp


@bp.route("/parties", methods=["GET"])
@token_required
def get_parties(user):
    """
    Get all available offices in the database
    :param user: token
    :return: http response
    """
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
    """
    Get a party by its id
    :param user: token
    :param id: party id
    """
    party = Party.get_party_by_id(id)
    if party:
        # if party is found
        resp = jsonify({"status": 200, "data": party, "message": "Party fetched successfully."})
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
    """
    Delete the party from database
    :param id: party id
    :param user: token
    """
    party = Party.get_party_by_id(id)
    if party:
        # after the getting the specific party by its id, delete retrieved party
        Party.delete_party(id)
        resp = jsonify({"status": 200, "message": "Party deleted successfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "message": "Delete failed. Party not found."})
        resp.status_code = 404
        return resp

@bp.route("/parties/<int:id>", methods=["PATCH"])
@token_required
def update_Party(user, id):
    """
    
    """
    data = request.get_json()
    try:
        party_name = data['name']
        hqaddress = data['hqaddress']
        logo_url = data['logo_url']
    except:
        # enforce use of appropriate keys
        resp = jsonify({"status": 400, "error": "Use appropriate keys."})
        resp.status_code = 400
        return resp
    if not party_name or not hqaddress or not logo_url:
        abort(make_response(jsonify({"error" : "Cannot update with empty fields", "status" : 400}), 400))
    party = Party.get_party_by_id(id)
    if party:
        Party.update_party(party_name=party_name, hqaddress=hqaddress, logo_url=logo_url, party_id=id)

        # after the getting the specific Party by its id, delete retrieved Party
        resp = jsonify({"status": 200, "message": "Party updated successfully."})
        resp.status_code = 200
        return resp
    else:
        resp = jsonify({"status": 404, "message": "Party not found."})
        resp.status_code = 404
        return resp
