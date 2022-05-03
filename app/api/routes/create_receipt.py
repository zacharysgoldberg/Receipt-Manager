from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import check_datetime, update_total
from flask_login import login_required
from .login import bp
from ..commands import existing_year, new_year

# Create new receipt

# Require user to be logged in before adding a receipt


@ bp.route('/logged_in/<id>/add_receipt', methods=['POST'])
@ login_required
def add_receipt(id: int):
    User.query.get_or_404(id)

    lst = ['purchase_total', 'tax', 'city', 'state', 'date_time']
    if any(item not in request.json for item in lst) \
            or type(request.json['purchase_total']) != float\
            or type(request.json['tax']) != float \
            or request.json['city'].isalpha() == False \
            or request.json['state'].isalpha() == False \
            or check_datetime(request.json['date_time']) == False:
        return abort(400)

    try:
        # add new receipt to existing tax year total
        receipt = existing_year.existing_year(id)
        return jsonify(receipt.serialize())

    except:
        # add new receipt to new tax year total
        receipt = new_year.new_year(id)
        return jsonify(receipt.serialize())
