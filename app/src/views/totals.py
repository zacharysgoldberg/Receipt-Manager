from flask import Blueprint, jsonify, abort, request
from ..models.models import Total, db, Receipt, User
from datetime import datetime, date


bp = Blueprint('totals', __name__, url_prefix='/totals')


# Get

# Get all totals
@bp.route('', methods=['GET'])
def get_totals():
    totals = Total.query.all()
    result = []
    for total in totals:
        result.append(total.serialize())

    return jsonify(result)

# Get a tax year totals


@bp.route('/<int:id>', methods=["GET"])
def get_total(id: int):
    total = Total.query.get_or_404(id)
    return jsonify(total.serialize())

# Get totals for user


@bp.route('/<int:id>/totals_stored')
def totals_stored(id: int):
    user = User.query.get_or_404(id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)

# Get totals for receipt


@bp.route('/<int:id>/receipt_totals')
def receipt_totals(id: int):
    total = Total.query.get_or_404(id)
    result = [receipt.serialize() for receipt in total.receipt_totals]
    return jsonify(result)


# Delete


@ bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    total = Total.query.get_or_404(id)

    try:
        db.session.delete(total)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
