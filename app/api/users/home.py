from flask_jwt_extended import jwt_required
from flask import Blueprint, render_template
from .users_admin import bp


@bp.route("/home")
@jwt_required(optional=True)
def index():
    resp = "Welcome to Stub-Manager"
    return render_template('home.html')
