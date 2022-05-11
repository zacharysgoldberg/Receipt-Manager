from flask import Blueprint, jsonify, abort, request
from ..models.models import Total, db, Receipt, User
from flask_jwt_extended import jwt_required, get_jwt

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


@bp.route('/<_id>', methods=["GET"])
def get_total(_id: int):
    total = Total.query.get_or_404(_id)
    return jsonify(total.serialize())

# Get totals for user


@bp.route('/<_id>/totals_stored')
def totals_stored(_id: int):
    user = User.query.get_or_404(_id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)

# Get totals for receipt


@bp.route('/<_id>/receipt_totals')
def receipt_totals(_id: int):
    total = Total.query.get_or_404(_id)
    result = [receipt.serialize() for receipt in total.receipt_totals]
    return jsonify(result)


# Delete


@ bp.route('/<_id>', methods=['DELETE'])
@jwt_required()
def delete(_id: int):
    claims = get_jwt()
    if not claims['is_admin']:
        return jsonify({"message": "Must be admin to fullfil request"}), 401
    total = Total.query.get_or_404(_id)
    receipt_id = db.session.query(Receipt._id).filter(
        Receipt.total_id == _id).first()[0]
    receipt = Receipt.query.get(receipt_id)

    try:
        db.session.delete(total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
