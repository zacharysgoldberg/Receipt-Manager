from flask_jwt_extended import jwt_required
from flask import Blueprint

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route("")
@jwt_required()
def index():
    resp = "Welcome to Homepage"
    return resp
