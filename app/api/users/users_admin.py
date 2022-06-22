from api.commands.access_level import admin_required
from flask import Blueprint, jsonify
from ..models import User, db

bp = Blueprint('users', __name__, url_prefix='/users')


# [get all users]


@bp.route('', methods=['GET'])
@admin_required()
def get_users():
    users = User.query.all()
    result = [u.serialize() for u in users]
    return jsonify(result)

# [get a user]


@bp.route('/<_id>', methods=['GET'])
@admin_required()
def get_user(_id: int):
    user = User.query.get_or_404(_id)
    return jsonify(user.serialize())


@bp.route('/delete_user/<_id>', methods=['DELETE'])
@admin_required()
def delete_user(_id: int):
    try:
        user = User.query.get_or_404(_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'deleted_user': user.serialize()})

    except BaseException as error:
        return jsonify({'error': error})
