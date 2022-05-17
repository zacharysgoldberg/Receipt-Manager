from ..login.home_page import bp
from ..models import User
from ..commands import existing_year, new_year
from ..commands.validate import validate_datetime
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import jsonify, request


# [create new receipt]


@ bp.route('/add_receipt', methods=['POST'])
@jwt_required(fresh=True)
def add_receipt():
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        User.query.get_or_404(user_id)

        lst = {'from', 'purchase_total', 'tax', 'address', 'date_time'}
        if any(item not in data for item in lst) \
                or not isinstance(data['from'], str) \
                or not isinstance(data['purchase_total'], float)\
                or not isinstance(data['tax'], float) \
                or not isinstance(data['address'], str) \
                or not isinstance(data['cash'], bool) \
                or (isinstance(data['card_last_4'], int) and len(data['card_last_4']) == 4) \
                or validate_datetime('datetime', data['date_time']) == False:

            return jsonify({"error": "One of more conditions did not meet parsing requirements"})

        # [add new receipt to existing tax year total]
        receipt = existing_year.existing_year(
            user_id, int(data['date_time'][6:10]))
        return jsonify(receipt.serialize())

    except BaseException:
        # [add new receipt to new tax year total]
        receipt = new_year.new_year(user_id)
        return jsonify(receipt.serialize())
