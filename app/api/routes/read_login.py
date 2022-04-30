from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import User
from flask_login import login_required
from .login import bp

# Get all receipts stored by user


@ bp.route('/logged_in/<int:id>/receipts_stored', methods=['GET'])
@ login_required
def receipts_stored(id: int):
    user = User.query.get_or_404(id)
    result = [receipt.serialize() for receipt in user.receipts_stored]
    return jsonify(result)


# Get all totals for user


@ bp.route('/logged_in/<int:id>/totals_stored', methods=['GET'])
@ login_required
def totals_stored(id: int):
    user = User.query.get_or_404(id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)
