from flask import Flask, Blueprint, jsonify, request
from api.v2.views import bp
from flask import abort, make_response, jsonify, request


from api.v2.models.models import Votes
from api.v2.utils.helpers import token_required, decode_token



@bp.route("/votes/<int:candidate_id>", methods=["POST"])
@token_required
def voting(user, candidate_id):

    data = request.get_json()
    try:
        candidate_voted_For = data["candidate_voted_For"]
        created_by = data["created_by"]
        office_voted_for = data["office_voted_for"]

    except KeyError:
        resp = jsonify({"status": 400, "error": "All fields required."})
        resp.status_code = 400
        return resp
    voted = Votes.check_that_user_has_voted(created_by, office_voted_for)
    if voted:
        abort(make_response(jsonify({"error": "You have already cast your vote", "status": 401}, 401)))

    username = decode_token()
    vote = Votes(createBy=username, candidateVoteFor=candidate_id, officeVotedFor=office_voted_for)

    vote.create_vote()
    resp = jsonify({"status": 201, "message": "Vote cast successfully."}), 201
    
    return resp
