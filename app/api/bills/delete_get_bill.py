from flask import jsonify, request
from ..models import Bill, User, db
from ..users.get_users import bp
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from .add_bill import bp


@bp.route('/bills', methods=['GET'])
@ bp.route('/bills/<bill_id>', methods=['DELETE'])
@ jwt_required(fresh=True)
def get_remove_bills(bill_id=None):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if request.method == 'GET':
        result = [bill.serialize() for bill in user.bills_stored]
        return jsonify(result)

    elif request.method == 'DELETE':
        bill = Bill.query.get(bill_id)
        db.session.delete(bill)
        db.session.commit()
        return jsonify({'removed': bill.serialize()})
