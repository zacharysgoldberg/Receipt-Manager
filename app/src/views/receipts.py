from flask import Blueprint, jsonify, abort, request
from ..models import Receipt, receipts_totals, Total, db, User
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

# get a receipt from user


@bp.route('/<int:id>')
def get_receipt(id: int):
    receipt = Receipt.query.get_or_404(id)
    return jsonify(receipt.serialize())

# Create new user


def check_datetime(date_time):
    try:
        dt = datetime.strptime(date_time, "%m-%d-%Y %H:%M")
        return True
    except ValueError:
        return False


def update_total(t, total, year, purchase_total, tax, user_id):
    # update totals for associated tax year if tax year input exists
    if int(year) == total.tax_year and t == 'add':
        total.purchase_totals = float(
            total.purchase_totals) + float(purchase_total)
        total.tax_totals = float(total.tax_totals) + float(tax)

    elif int(year) == total.tax_year and t == 'update_purchase':
        total.purchase_totals = float(
            total.purchase_totals) + float(purchase_total)

    elif int(year) == total.tax_year and t == 'update_tax':
        total.tax_totals = float(total.tax_totals) + float(tax)

    # add receipt to new total for new tax year if tax year input does not exist
    else:
        total = Total(
            purchase_totals=purchase_total,
            tax_totals=tax,
            tax_year=year,
            user_id=user_id
        )
        db.session.add(total)


@ bp.route('', methods=['POST'])
def add_receipt():
    lst = ['purchase_total', 'tax', 'city', 'state', 'date_time']
    if any(item not in request.json for item in lst) \
            or type(request.json['purchase_total']) != float\
            or type(request.json['tax']) != float \
            or request.json['city'].isalpha() == False \
            or request.json['state'].isalpha() == False \
            or check_datetime(request.json['date_time']) == False:
        return abort(400)

    total_id = db.session.query(Total.id).filter(
        Total.user_id == request.json['user_id']).first()[0]
    total = Total.query.get(total_id)
    update_total('add', total, request.json['date_time'][6:10],
                 request.json['purchase_total'], request.json['tax'], _)

    receipt = Receipt(
        purchase_total=request.json['purchase_total'],
        tax=request.json['tax'],
        city=request.json['city'],
        state=request.json['state'],
        transacton_num=str(request.json['transaction_num']) if 'transaction_num' in request.json and str(request.json['transaction_num']).isnumeric(
        ) == True else None,
        description=request.json['description'] if 'description' in request.json else None,
        date_time=request.json['date_time'],
        total_id=db.session.query(Total.id).filter(
            Total.user_id == request.json['user_id']).first()[0],
        user_id=request.json['user_id']
    )

    db.session.add(receipt)
    db.session.commit()

    return jsonify(receipt.serialize())

# Delete user


@ bp.route('/<int:id>', methods=['DELETE'])
def delete_receipt(id: int):
    receipt = Receipt.query.get_or_404(id)
    try:
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)


# Update receipt


"""@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update_receipt(id: int):
    receipt = Receipt.query.get_or_404(id)
    lst = ['purchase_total', 'tax', 'city', 'state',
           'transaction_num', 'description', 'date_time']
    if all(item not in request.json for item in lst):
        return abort(400)

    if 'purchase_total' in request.json:
        if type(request.json['purchase_total']) != float:
            return abort(400)

        receipt.purchase_total = request.json['purchase_total']
        total_id = db.session.query(Total.id).filter(
            Total.user_id == ).first()[0]
        total = Total.query.get(total_id)
        update_total(total)

    if 'tax' in request.json:
        if type(request.json['tax']) != float:
            return abort(400)

        receipt.tax = request.json['tax']
        total_id = db.session.query(Total.id).filter(
            Total.user_id == ).first()[0]
        total = Total.query.get(total_id)
        update_total(total)

    if 'city' in request.json:
        if len(request.json['city']) < 2:
            return abort(400)

        receipt.city = request.json['city']

    if 'state' in request.json:
        if len(request.json['state']) != 2:
            return abort(400)

        receipt.state = request.json['state']

    if 'transaction_num' in request.json:
        if str(request.json['transaction_num']).isnumeric() == False:
            return abort(400)

        receipt.transaction_num = request.json['transaction_num']

    if 'description' in request.json:
        if type(request.json['description']) != str:
            return abort(400)

        receipt.description = request.json['description']

    if 'date_time' in request.json:
        if check_datetime(request.json['date_time']) == False:
            return abort(400)

        receipt.date_time = request.json['date_time']

    try:
        db.session.commit()
        return jsonify(receipt.serialize())

    except:
        return jsonify(False)
"""
# Tips that a user submitted


"""@ bp.route('/<int:id>/tips_submitted', methods=['GET'])
def tips_submitted(id: int):
    user = User.query.get_or_404(id)
    result = [tip.serialize() for tip in user.tips_submitted]
    return jsonify(result)"""

# Content that a user liked


@ bp.route('/<int:id>/liked_content', methods=['GET'])
def liked_content(id: int):
    user = User.query.get_or_404(id)
    result = [content.serialize() for content in user.liked_content]
    return jsonify(result)

# Like content


@ bp.route('/<int:id>/like', methods=['POST'])
def like(id: int):
    if 'content_id' not in request.json:
        return abort(400)

    User.query.get_or_404(id)
    Content.query.get_or_404(request.json['content_id'])

    try:
        like = sqlalchemy.insert(users_content).values(
            user_id=id, content_id=request.json['content_id'])
        db.session.execute(like)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

# Unlike content


@ bp.route('/<int:user_id>/unlike/<int:content_id>', methods=['DELETE'])
def unlike(user_id: int, content_id: int):
    # check user and content exist
    User.query.get_or_404(user_id)
    Content.query.get_or_404(content_id)

    try:
        unlike = sqlalchemy.delete(users_content).where(
            users_content.c.user_id == user_id,
            users_content.c.content_id == content_id
        )
        db.session.execute(unlike)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
