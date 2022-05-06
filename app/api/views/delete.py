from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import subtract_from_total
from flask_login import login_required, logout_user
from .login import bp

# Delete

# Remove user


@ bp.route('/logged_in/<username>', methods=['DELETE'])
@ login_required
def delete_user(username: str):
    try:
        user_id = db.session.query(User.id).filter(
            User.username == username).first()[0]
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return jsonify(True)

    except:
        return jsonify(False)

# Remove receipt


@ bp.route('/logged_in/<username>/remove_receipt/<receipt_id>', methods=['DELETE'])
@ login_required
def delete_receipt(username: str, receipt_id: int):
    # check user and content exist
    user_id = db.session.query(User.id).filter(
        User.username == username).first()[0]
    User.query.get_or_404(user_id)

    receipt = Receipt.query.get_or_404(receipt_id)
    tax_year = str(receipt.date_time)[0:4]
    total_id = db.session.query(Total.id).filter(
        Total.tax_year == tax_year).first()[0]
    total = Total.query.get(total_id)

    try:
        # Subtract removed receipt amount from total
        subtract_from_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)

    except:
        return jsonify(False)
