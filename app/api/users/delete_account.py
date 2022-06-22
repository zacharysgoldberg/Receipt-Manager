from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from ..models import User, db
from .users_admin import bp

# [remove user]


@ bp.route('/home/delete_account', methods=['DELETE'])
@jwt_required(fresh=True)
def delete_account():
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'deleted_account': user.serialize()})

    except BaseException as error:
        return jsonify({'error': error})
