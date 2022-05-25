from ..users.home_page import bp
from flask import jsonify, render_template
from ..models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# [get all receipts stored by user]


@ bp.route('/receipts_stored', methods=['GET'])
# @jwt_required()
def receipts_stored():
    # user_id = get_jwt_identity()
    user = User.query.get_or_404(1)
    receipts = [receipt.serialize() for receipt in user.receipts_stored]
    for receipt in receipts:
        for el in receipt.items():
            if 'date_time' in el:
                # print('DATE TIME!', str(el[1])[0:10])
                receipt['date_time'] = str(el[1])[0:9]

    return jsonify(receipts)
    # return render_template('receipts.html', receipts=receipts)


# [get all totals for user]


@ bp.route('/totals_stored', methods=['GET'])
@ jwt_required()
def totals_stored():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)
