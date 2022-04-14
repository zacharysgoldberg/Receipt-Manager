# add handlers for user input and import variables from player_class/game_class
from flask import Blueprint, jsonify, abort, request
from ..models import Total, User, Receipt, db
from .receipts import check_datetime, update_total
import re
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

# from ..blackjack_modules.game_class import user_login, successful

bp = Blueprint('users', __name__, url_prefix='/users')


def check_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    if regex.fullmatch(email):
        return True

    else:
        return False


def confirm_user(username):
    # for postgres db
    exists = db.session.query(User.id).filter(
        User.username == username).first()
    return exists


def subtract_old_total(t, receipt, total):
    if t == 'purchase':
        total.purchase_totals = float(
            total.purchase_totals) - float(receipt.purchase_total)
    elif t == 'tax':
        total.tax_totals = float(total.tax_totals) - float(receipt.tax)

    db.session.commit()

# Read

# Get all users


@bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [u.serialize() for u in users]
    return jsonify(result)

# Get a user


@bp.route('/<int:id>')
def get_user(id: int):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


@ bp.route('/<int:id>/receipts', methods=['GET'])
def user_receipts(id: int):
    user = User.query.get_or_404(id)
    result = [user.serialize() for user in user.receipts]
    return jsonify(result)


# Create

# Create a user
@bp.route('', methods=['POST'])
def create_user():
    # if successful == False:
    length = [len(request.json['username']), len(request.json['password'])]
    lst = ['username', 'password', 'firstname', 'lastname', 'email']

    if length[0] < 3 or length[1] < 8 \
            or any(item not in request.json for item in lst) \
            or check_email(request.json['email'].strip()) == False \
            or confirm_user(request.json['username'].strip().replace(" ", "")) is not None\
            or request.json['firstname'].strip().isalpha() == False \
            or request.json['lastname'].strip().isalpha() == False:
        return abort(400)

    user = User(
        firstname=request.json['firstname'].title().strip(),
        lastname=request.json['lastname'].title().strip(),
        username=request.json['username'].strip().replace(
            " ", ""),
        password=generate_password_hash(
            request.json['password'].strip().replace(" ", "")),
        email=request.json['email'].strip()
    )

    db.session.add(user)
    db.session.commit()

    total = Total(
        purchase_totals=0.00,
        tax_totals=0.00,
        tax_year=datetime.now().year,
        user_id=db.session.query(User.id).filter(
            User.username == request.json['username']).first()[0]
    )

    db.session.add(total)
    db.session.commit()

    return jsonify(user.serialize())


# Update


@ bp.route('/<int:id>', methods=['PATCH'])
def update_user(id: int):
    user = User.query.get_or_404(id)
    lst = ['username', 'password', 'email', 'firstname', 'lastname']
    if all(item not in request.json for item in lst):
        return abort(400)

    if 'firstname' in request.json:
        if request.json['firstname'].strip().isalpha() == False:
            return abort(400)
        user.firstname = request.json['firstname'].title().strip()

    if 'lastname' in request.json:
        if request.json['lastname'].strip().isalpha() == False:
            return abort(400)
        user.lastname = request.json['lastname'].title().strip()

    if 'username' in request.json:
        if len(request.json['username']) < 3:
            return abort(400)
        user.username = request.json['username'].strip().replace(" ", "")

    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        user.password = generate_password_hash(
            request.json['password'].strip().replace(" ", ""))

    if 'email' in request.json:
        if check_email(request.json['email'].strip()) == False:
            return abort(400)
        user.email = request.json['email'].strip()

    try:
        db.session.commit()
        return jsonify(user.serialize())

    except:
        return jsonify(False)


@bp.route('/<int:user_id>/receipts/<int:receipt_id>', methods=['PATCH', 'PUT'])
def update_receipt(user_id: int, receipt_id: int):
    receipt = Receipt.query.get_or_404(receipt_id)
    total_id = db.session.query(Total.id).filter(
        Total.user_id == user_id).first()[0]
    total = Total.query.get(total_id)
    lst = ['purchase_total', 'tax', 'city', 'state',
           'transaction_num', 'description', 'date_time']
    if all(item not in request.json for item in lst):
        return abort(400)

    if 'purchase_total' in request.json:
        if type(request.json['purchase_total']) != float:
            return abort(400)

        subtract_old_total('purchase', receipt, total)
        receipt.purchase_total = request.json['purchase_total']
        db.session.commit()
        update_total('update_purchase', total, total.tax_year,
                     receipt.purchase_total, _, _)

    if 'tax' in request.json:
        if type(request.json['tax']) != float:
            return abort(400)

        subtract_old_total('tax', receipt, total)
        receipt.tax = request.json['tax']
        db.session.commit()
        update_total('update_tax', total, total.tax_year,
                     _, receipt.tax, _)

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


# Delete

@ bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id: int):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
