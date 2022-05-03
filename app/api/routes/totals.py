from flask import Blueprint, jsonify, abort, request
from ..models.models import Total, db, Receipt, User

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


@bp.route('/<id>', methods=["GET"])
def get_total(id: int):
    total = Total.query.get_or_404(id)
    return jsonify(total.serialize())

# Get totals for user


@bp.route('/<id>/totals_stored')
def totals_stored(id: int):
    user = User.query.get_or_404(id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)

# Get totals for receipt


@bp.route('/<id>/receipt_totals')
def receipt_totals(id: int):
    total = Total.query.get_or_404(id)
    result = [receipt.serialize() for receipt in total.receipt_totals]
    return jsonify(result)


# Delete


@ bp.route('/<id>', methods=['DELETE'])
def delete(id: int):
    total = Total.query.get_or_404(id)
    receipt_id = db.session.query(Receipt.id).filter(
        Receipt.total_id == id).first()[0]
    receipt = Receipt.query.get(receipt_id)

    try:
        db.session.delete(total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
