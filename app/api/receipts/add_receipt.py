from ..commands import existing_year, new_year
from ..commands.validate import validate_datetime
from ..models import User, db
from ..login.home_page import bp
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import(
    jsonify,
    abort,
    request,
    redirect
)

# [create new receipt]


@ bp.route('/add_receipt', methods=['POST'])
@jwt_required(fresh=True)
def add_receipt():
    data = request.get_json()
    user_id = get_jwt_identity()
    User.query.get_or_404(user_id)

    lst = {'purchase_total', 'tax', 'city', 'state', 'date_time'}

    if any(item not in data for item in lst) \
            or not isinstance(data['purchase_total'], float)\
            or not isinstance(data['tax'], float) \
            or data['city'].isalpha() == False \
            or data['state'].isalpha() == False \
            or validate_datetime('datetime', data['date_time']) == False:
        return abort(400)

    try:
        # [add new receipt to existing tax year total]
        receipt = existing_year.existing_year(
            user_id, int(data['date_time'][6:10]))
        return jsonify(receipt.serialize())

    except BaseException:
        # [add new receipt to new tax year total]
        receipt = new_year.new_year(user_id)
        return jsonify(receipt.serialize())
