from flask import Blueprint, jsonify, abort, request
from ..models.models import Receipt, Total, db, User
from ..commands.commands import subtract_old_total
from datetime import datetime

bp = Blueprint('receipts', __name__, url_prefix='/receipts')

# Get all receipts from user


@bp.route('', methods=['GET'])
def get_receipts():
    receipts = Receipt.query.all()
    result = []
    for receipt in receipts:
        result.append(receipt.serialize())
    return jsonify(result)

# get a receipt


@bp.route('/<int:id>')
def get_receipt(id: int):
    receipt = Receipt.query.get_or_404(id)
    return jsonify(receipt.serialize())

# Get receipts for user


@bp.route('/<int:id>/users_receipts', methods=['GET'])
def users_receipts(id: int):
    receipt = Receipt.query.get_or_404(id)
    result = [user.serialize() for user in receipt.users_receipts]
    return jsonify(result)


# Delete receipt


@ bp.route('/<int:id>', methods=['DELETE'])
def delete_receipt(id: int):
    receipt = Receipt.query.get_or_404(id)

    try:
        tax_year = str(receipt.date_time)[0:4]
        total_id = db.session.query(Total.id).filter(
            Total.tax_year == tax_year).first()[0]
        total = Total.query.get(total_id)
        # Subtract removed receipt amount from total
        subtract_old_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
