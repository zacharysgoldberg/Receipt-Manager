from ..users.home_page import bp
from ..models import User
from ..commands import existing_year
from ..commands import new_year
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request


# [create new receipt]


@ bp.route('/add_receipt', methods=['POST'])
@jwt_required(fresh=True)
def add_receipt():
    data = request.get_json()
    try:
        user_id = get_jwt_identity()
        User.query.get_or_404(user_id)

        # [add new receipt to existing tax year total]
        receipt = existing_year.existing_year(
            user_id, int(data['date_time'][6:10]))
        return jsonify(receipt.serialize())

    except BaseException:
        # [add new receipt to new tax year total]
        receipt = new_year.new_year(user_id)
        return jsonify(receipt.serialize())
