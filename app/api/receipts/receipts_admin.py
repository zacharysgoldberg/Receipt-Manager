from api.commands.access_level import admin_required
from flask import Blueprint, jsonify
from ..models import Receipt, Total, db
from ..commands.subtract_from_total import subtract_from_total
from flask_jwt_extended import jwt_required, get_jwt

bp = Blueprint('receipts', __name__, url_prefix='/receipts')

# [get all receipts from user]


@bp.route('', methods=['GET'])
@admin_required()
def get_receipts():
    receipts = Receipt.query.all()
    result = []
    for receipt in receipts:
        result.append(receipt.serialize())
    return jsonify(result)

# [get a receipt]


@bp.route('/<_id>')
@admin_required()
def get_receipt(_id: int):
    receipt = Receipt.query.get_or_404(_id)
    return jsonify(receipt.serialize())

# [get receipts for user]


@bp.route('/<_id>/users_receipts', methods=['GET'])
@admin_required()
def users_receipts(_id: int):
    receipt = Receipt.query.get_or_404(_id)
    result = [user.serialize() for user in receipt.users_receipts]
    return jsonify(result)


# [delete receipt]


@ bp.route('/<_id>', methods=['DELETE'])
@admin_required()
def delete_receipt(_id: int):
    receipt = Receipt.query.get_or_404(_id)

    try:
        # [formatting tax year from date and time column]
        tax_year = str(receipt.date_time)[0:4]
        total_id = db.session.query(Total._id).filter(
            Total.tax_year == tax_year).first()[0]
        total = Total.query.get(total_id)
        # [subtract removed receipt amount from total]
        subtract_from_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify({"deleted": receipt.serialize()})
    except BaseException as error:
        return jsonify({"error": error})
