from flask import Blueprint, jsonify, request, abort
from ..models import Bill, User, db
from ..commands.validate import validate_datetime
from ..login.home_page import bp
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from datetime import datetime


@bp.route('/bills/add_bill', methods=['POST'])
@jwt_required(fresh=True)
def add_bill():
    data = request.get_json()

    lst = {'issuer', 'balance', 'date_issued',
           'amount_due', 'due_date', 'invoice_number', 'paid'}

    if any(item not in data for item in lst) \
            or not isinstance(data['issuer'], str) \
            or not isinstance(data['balance'], float) \
            or validate_datetime('date', data['date_issued']) == False \
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

        issuer = data['issuer']
        balance = data['balance']
        date_issued = data['date_issued']
        amount_due = data['amount_due']
        fees = data['fees'] if 'fees' in data else None
        interest = data['interest'] if 'interest' in data else None
        due_date = data['due_date']
        invoice_number = data['invoice_number']
        description = data['description'] if 'description' in data else None
        paid = data['paid']
        past_due = False if datetime.now().strftime(
            '%m/%d/%Y') <= due_date else True

        new_bill = Bill.add_bill(
            issuer, balance, date_issued,
            amount_due, fees, interest, due_date,
            invoice_number, description, paid, past_due, user_id
        )

        return jsonify(new_bill.serialize())

    except BaseException as error:
        return jsonify({'error': error})
