# add handlers for user input and import variables from player_class/game_class
from flask import Blueprint, jsonify, abort, request
from ..models import Total, User, Receipt, db
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
