from api.commands.access_level import admin_required
from flask import Blueprint, jsonify, request
from ..models import Receipt, Total, User, db

bp = Blueprint('totals', __name__, url_prefix='/totals')


# [get all totals]
@bp.route('', methods=['GET'])
@admin_required()
def get_totals():
    totals = Total.query.all()
    result = []
    for total in totals:
        result.append(total.serialize())

    return jsonify(result)

# [GET or DELETE a tax year total]


@bp.route('/<_id>', methods=['GET', 'DELETE'])
@admin_required()
def get_or_delete_total(_id: int):
    if request.method == 'GET':
        total = Total.query.get_or_404(_id)
        return jsonify(total.serialize())

    elif request.method == 'DELETE':
        total = Total.query.get_or_404(_id)
        receipt_id = db.session.query(Receipt._id).filter(
            Receipt.total_id == _id).first()[0]
        receipt = Receipt.query.get(receipt_id)

        try:
            db.session.delete(total)
            db.session.delete(receipt)
            db.session.commit()
            return jsonify({"deleted": total.serialize()})
        except BaseException as error:
            return jsonify({"error": error})


# [get totals for user]


@bp.route('/<_id>/totals_stored')
@admin_required()
def totals_stored(_id: int):
    user = User.query.get_or_404(_id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)

# [get totals for receipt]


@bp.route('/<_id>/receipt_totals')
@admin_required()
def receipt_totals(_id: int):
    total = Total.query.get_or_404(_id)
    result = [receipt.serialize() for receipt in total.receipt_totals]
    return jsonify(result)
