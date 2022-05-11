from flask import Blueprint, jsonify, abort, request
from ..models.models import Total, User, db
from ..commands.security import validate_email, check_email
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


@bp.route('/<_id>', methods=['GET'])
def get_user(_id: int):
    user = User.query.get_or_404(_id)
    return jsonify(user.serialize())


# Create

# Create a user
@bp.route('/register', methods=['POST'])
def register():
    lst = ['password', 'firstname', 'lastname', 'email']
    data = request.get_json()
    # Checking if
    if len(data['password']) < 8 \
            or any(item not in data for item in lst) \
            or data['firstname'].strip().isalpha() == False \
            or data['lastname'].strip().isalpha() == False:
        return abort(400)

    email = data['email'].strip().replace(" ", "")
    # Checking if email exists in db
    if validate_email(email) is not None:
        return 'Email already exists'
    # Checking email is in a valid format
    elif check_email(email) == False:
        return 'Email is already in use'

    password = data['password'].strip().replace(" ", "")
    # Add new user
    email = data['email'].strip()
    user = User(
        firstname=data['firstname'].capitalize().strip(),
        lastname=data['lastname'].capitalize().strip(),
        password=generate_password_hash(password),
        email=email,
        username=email.split('@')[0])

    db.session.add(user)
    db.session.commit()

    total = Total(
        purchase_totals=0.00,
        tax_totals=0.00,
        tax_year=datetime.now().year,
        user_id=db.session.query(User.id).filter(
            User.email == data['email']).first()[0]
    )

    db.session.add(total)
    db.session.commit()
    return jsonify(user.serialize())
