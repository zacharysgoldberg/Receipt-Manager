from flask import Blueprint, jsonify, abort, request
from ..models.models import Receipt, Total, db, User
from ..commands.commands import subtract_from_total
from flask_jwt_extended import jwt_required, get_jwt
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


@bp.route('/<_id>')
def get_receipt(_id: int):
    receipt = Receipt.query.get_or_404(_id)
    return jsonify(receipt.serialize())

# Get receipts for user


@bp.route('/<_id>/users_receipts', methods=['GET'])
def users_receipts(_id: int):
    receipt = Receipt.query.get_or_404(_id)
    result = [user.serialize() for user in receipt.users_receipts]
    return jsonify(result)


# Delete receipt


@ bp.route('/<_id>', methods=['DELETE'])
@jwt_required
def delete_receipt(_id: int):
    claims = get_jwt()
    if not claims['is_admin']:
        return jsonify({"message": "Must be admin to fullfil request"})
    receipt = Receipt.query.get_or_404(_id)

    try:
        # Formatting tax year from date and time column
        tax_year = str(receipt.date_time)[0:4]
        total_id = db.session.query(Total.id).filter(
            Total.tax_year == tax_year).first()[0]
        total = Total.query.get(total_id)
        # Subtract removed receipt amount from total
        subtract_from_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
