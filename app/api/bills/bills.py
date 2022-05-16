import re
from flask import Blueprint, jsonify, request, abort
from ..models import Bill, User, db
from ..commands.validate import validate_datetime
from ..users.get_users import bp
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime


@bp.route('/bills/add_bill', methods=['POST'])
@jwt_required(fresh=True)
def add_bill():
    data = request.get_json()

    lst = {'issuer', 'balance', 'date_of_issuance',
           'amount_due', 'due_date', 'invoice_number', 'paid'}

    if any(item not in data for item in lst) \
            or not isinstance(data['issuer'], str) \
            or not isinstance(data['balance'], float) \
            or validate_datetime('date', data['date_of_issuance']) == False \
            or validate_datetime('date', data['due_date']) == False \
            or not isinstance(data['amount_due'], float) \
            or not isinstance(data['invoice_number'], int) \
            or ('fees' in data and not isinstance(data['fees'], float)) \
            or ('interest' in data and not isinstance(data['interest'], float)) \
            or ('description' in data and not isinstance(data['description'], str)) \
            or not isinstance(data['paid'], bool):
        return abort(400)

    try:
        user_id = get_jwt_identity()
        User.query.get(user_id)

        bill = Bill(
            issuer=data['issuer'],
            balance=data['balance'],
            date_of_issuance=data['date_of_issuance'],
            amount_due=data['amount_due'],
            fees=data['fees'] if 'fees' in data else None,
            interest=data['interest'] if 'interest' in data else None,
            due_date=data['due_date'],
            invoice_number=data['invoice_number'],
            description=data['description'] if 'description' in data else None,
            paid=data['paid'],
            past_due=False if datetime.now().strftime(
                '%m/%d/%Y') <= data['due_date'] else True,
            user_id=user_id
        )

        db.session.add(bill)
        db.session.commit()
        return jsonify(bill.serialize())

    except BaseException as error:
        return jsonify({'error': error})


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
