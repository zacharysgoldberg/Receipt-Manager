from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import check_datetime, update_total
from flask_login import login_required
from .login import bp
from ..commands import existing_year, new_year

# Create new receipt

# Require user to be logged in before adding a receipt


@ bp.route('/logged_in/<username>/add_receipt', methods=['POST'])
@ login_required
def add_receipt(username: str):
    data = request.get_json()

    user_id = db.session.query(User.id).filter(
        User.username == username).first()[0]
    User.query.get_or_404(user_id)

    lst = ['purchase_total', 'tax', 'city', 'state', 'date_time']

    if any(item not in data for item in lst) \
            or type(data['purchase_total']) != float\
            or type(data['tax']) != float \
            or data['city'].isalpha() == False \
            or data['state'].isalpha() == False \
            or check_datetime(data['date_time']) == False:
        return abort(400)

    try:
        # add new receipt to existing tax year total
        receipt = existing_year.existing_year(
            user_id, int(data['date_time'][6:10]))
        return jsonify(receipt.serialize())

    except:
        # add new receipt to new tax year total
        receipt = new_year.new_year(user_id)
        return jsonify(receipt.serialize())
