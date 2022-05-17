from flask import(
    Blueprint,
    jsonify,
    abort,
    request,
    redirect,
    render_template,
    url_for
)
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route("")
@jwt_required()
def index():
    resp = "Welcome to Homepage"
    return resp  # render_template('home.html')
