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

