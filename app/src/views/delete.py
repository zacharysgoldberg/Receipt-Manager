from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import subtract_old_total
from flask_login import login_required, logout_user
from .login import bp

# Delete

# Remove user


@ bp.route('/logged_in/<int:id>', methods=['DELETE'])
@ login_required
def delete_user(id: int):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return jsonify(True)
    except:
        return jsonify(False)

# Remove receipt


@ bp.route('/logged_in/<int:user_id>/remove_receipt/<int:receipt_id>', methods=['DELETE'])
@ login_required
def delete_receipt(user_id: int, receipt_id: int):
    # check user and content exist
    User.query.get_or_404(user_id)
    receipt = Receipt.query.get_or_404(receipt_id)
    tax_year = str(receipt.date_time)[0:4]
    total_id = db.session.query(Total.id).filter(
        Total.tax_year == tax_year).first()[0]
    total = Total.query.get(total_id)

    try:
        # Subtract removed receipt amount from total
        subtract_old_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)

    except:
        return jsonify(False)
