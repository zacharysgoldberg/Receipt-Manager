# add handlers for user input and import variables from player_class/game_class
from flask import Blueprint, jsonify, abort, request
from ..models.models import Total, User, db
from ..commands.commands import confirm_email, check_email
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('users', __name__, url_prefix='/users')

# Read

# Get all users


@bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [u.serialize() for u in users]
    return jsonify(result)

# Get a user


@bp.route('/<id>', methods=['GET'])
def get_user(id: int):
    user = User.query.get_or_404(id)
    return jsonify(user.serialize())


# Create

# Create a user
@bp.route('', methods=['POST'])
def create_user():
    lst = ['password', 'firstname', 'lastname', 'email']
    # Checking if
    if len(request.json['password']) < 8 \
            or any(item not in request.json for item in lst) \
            or request.json['firstname'].strip().isalpha() == False \
            or request.json['lastname'].strip().isalpha() == False:
        return abort(400)

    email = request.json['email'].strip().replace(" ", "")
    # Checking if email exists in db
    if confirm_email(email) is not None:
        return 'Email already exists'
    # Checking email is in a valid format
    elif check_email(email) == False:
        return 'Email is already in use'

    password = request.json['password'].strip().replace(" ", "")
    # Add new user
    user = User(
        firstname=request.json['firstname'].capitalize().strip(),
        lastname=request.json['lastname'].capitalize().strip(),
        password=generate_password_hash(password),
        email=request.json['email'].strip(),
        authenticated=False)

    db.session.add(user)
    db.session.commit()

    total = Total(
        purchase_totals=0.00,
        tax_totals=0.00,
        tax_year=datetime.now().year,
        user_id=db.session.query(User.id).filter(
            User.email == request.json['email']).first()[0]
    )

    db.session.add(total)
    db.session.commit()
    return jsonify(user.serialize())
