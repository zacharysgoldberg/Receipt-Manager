from flask import Blueprint, jsonify, abort, request
from ..models.models import Receipt, Total, db, User
from ..commands.commands import check_datetime, update_total
import re
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


@ bp.route('/<int:id>/users_receipts', methods=['GET'])
def users_receipts(id: int):
    receipt = Receipt.query.get_or_404(id)
    result = [user.serialize() for user in receipt.users_receipts]
    return jsonify(result)


# Delete receipt


@ bp.route('/<int:id>', methods=['DELETE'])
def delete_receipt(id: int):
    receipt = Receipt.query.get_or_404(id)
    try:
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
