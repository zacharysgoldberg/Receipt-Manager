from flask_jwt_extended import jwt_required
from flask import render_template
from .users_admin import bp


@bp.route("/home")
@jwt_required()
def index():
    resp = "Welcome to Stub-Manager"
    return resp
