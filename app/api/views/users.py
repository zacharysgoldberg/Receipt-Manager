from flask import Blueprint, jsonify, abort, request
from ..models.models import Total, User, db
from ..commands.validate import validate_email
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('users', __name__, url_prefix='/users')


# [get all users]


@bp.route('', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [u.serialize() for u in users]
    return jsonify(result)

# [get a user]


@bp.route('/<_id>', methods=['GET'])
def get_user(_id: int):
    user = User.query.get_or_404(_id)
    return jsonify(user.serialize())


# [create a user]
@bp.route('/register', methods=['POST'])
def register():
    lst = ['password', 'firstname', 'lastname', 'email']
    data = request.get_json()
    # [ensure password is at least 8 characters in length]
    if len(data['password']) < 8 \
            or any(item not in data for item in lst) \
            or data['firstname'].strip().isalpha() == False \
            or data['lastname'].strip().isalpha() == False:
        return abort(400)

    email = data['email'].strip().replace(" ", "")
    # [check if email exists in db]
    if validate_email(email) is not None:
        return jsonify({'error': 'Email is already in use'})
    # [checking email is in a valid format]
    elif validate_email(email) == False:
        return jsonify({'error': 'Email format is incorrect'})

    password = data['password'].strip().replace(" ", "")
    # [add new user]
    email = data['email'].strip()
    user = User(
        firstname=data['firstname'].capitalize().strip(),
        lastname=data['lastname'].capitalize().strip(),
        password=generate_password_hash(password),
        email=email,
        username=email.split('@')[0])

    db.session.add(user)
    db.session.commit()

    # [add new total]
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
