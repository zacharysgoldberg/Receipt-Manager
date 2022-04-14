from flask import Blueprint, jsonify, abort, request
from ..models import Total, db, Receipt
from datetime import datetime, date
import sqlalchemy


bp = Blueprint('totals', __name__, url_prefix='/totals')


# Get


@bp.route('', methods=['GET'])
def index():
    totals = Total.query.all()
    result = []
    for total in totals:
        print("TOTAL!!!: ", total)
        # s = json.dumps(total, use_decimal=True)
        result.append(total.serialize())

    return jsonify(result)


@ bp.route('/<int:id>', methods=["GET"])
def show(id: int):
    total = Total.query.get_or_404(id)
    return jsonify(total.serialize())


# Delete
@ bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    total = Total.query.get_or_404(id)

    try:
        db.session.delete(total)  # prepare DELETE tip
        db.session.commit()  # execute DELETE tip
        return jsonify(True)
    except:
        return jsonify(False)

# User that submitted tip


@ bp.route('/<int:id>/submitted_tips', methods=['GET'])
def submitted_tips(id: int):
    tip = Tip.query.get_or_404(id)
    result = [user.serialize() for user in tip.submitted_tips]
    return jsonify(result)
