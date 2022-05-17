from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import(
    Blueprint,
    jsonify,
    redirect,
    render_template
)

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route("")
@jwt_required()
def index():
    resp = "Welcome to Homepage"
    return resp
