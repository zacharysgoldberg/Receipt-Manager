from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import User, db
from flask_login import login_required
from .login import bp

# Get all receipts stored by user


@ bp.route('/logged_in/<username>/receipts_stored', methods=['GET'])
@ login_required
def receipts_stored(username: str):
    user_id = db.session.query(User.id).filter(
        User.username == username).first()[0]
    user = User.query.get_or_404(user_id)
    result = [receipt.serialize() for receipt in user.receipts_stored]
    return jsonify(result)


# Get all totals for user


@ bp.route('/logged_in/<username>/totals_stored', methods=['GET'])
@ login_required
def totals_stored(username: str):
    user_id = db.session.query(User.id).filter(
        User.username == username).first()[0]
    user = User.query.get_or_404(user_id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)
