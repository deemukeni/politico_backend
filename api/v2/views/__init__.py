from flask import Blueprint

# use blueprint to version api endpoints
bp = Blueprint("apiv2", __name__, url_prefix="/api/v2")
# for versioning : evry route will have /api/v2 prefixon it
