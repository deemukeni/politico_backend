from flask import Flask, Blueprint, jsonify, request
from api.v2.views import bp

from api.v2.models.models import Votes
from api.v2.utils.helpers import token_required, decode_token



@bp.route("/votes/<int:candidate_id>", methods=["POST"])
@token_required
def voting(user, candidate_id):

    # data = request.get_json()
    # try:
    #     candidateVoteFor = data["candidateVoteFor"] 
    #     officeVotedFor = data["officeVotedFor"]

    # except KeyError:
    #     resp = jsonify({"status": 400, "error": "Please vote first."})
    #     resp.status_code = 400
    #     return resp
    

    username = decode_token()

    vote = Votes(createBy=username, candidateVoteFor=candidate_id, officeVotedFor=officeVotedFor)

    vote.create_vote()
    resp = jsonify({"status": 200, "mesage": "Vote cast successfully."}), 200
    
    return resp
