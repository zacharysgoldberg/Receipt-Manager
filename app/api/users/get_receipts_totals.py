from ..login.home_page import bp
from flask import jsonify
from ..models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

# [get all receipts stored by user]


@ bp.route('/receipts_stored', methods=['GET'])
@jwt_required()
def receipts_stored():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    result = [receipt.serialize() for receipt in user.receipts_stored]
    return jsonify(result)


# [get all totals for user]


@ bp.route('/totals_stored', methods=['GET'])
@jwt_required()
def totals_stored():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)
