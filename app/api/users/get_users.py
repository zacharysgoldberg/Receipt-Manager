from flask import Blueprint, jsonify
from ..models import User, db

bp = Blueprint('users', __name__, url_prefix='/users')


# [get all users]


@bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [u.serialize() for u in users]
    return jsonify(result)

# [get a user]


@bp.route('/<_id>', methods=['GET'])
def get_user(_id: int):
    user = User.query.get_or_404(_id)
    return jsonify(user.serialize())
