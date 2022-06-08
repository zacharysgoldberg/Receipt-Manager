from ..users.users_admin import bp
from flask import jsonify, render_template
from ..models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json

# [get all receipts stored by user]


@ bp.route('/home/receipts_stored', methods=['GET'])
@jwt_required()
def receipts_stored():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    receipts = [receipt.serialize() for receipt in user.receipts_stored]
    resp = render_template('receipts.html', jsonfile=json.dumps(receipts))
    json_resp = jsonify(receipts)
    return json_resp


# [get all totals for user]


@ bp.route('/home/totals_stored', methods=['GET'])
@ jwt_required()
def totals_stored():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    result = [total.serialize() for total in user.totals_stored]
    json_resp = jsonify(result)
    return json_resp
