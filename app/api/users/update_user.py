from ..models import User, db
from ..commands.validate import validate_email
from werkzeug.security import generate_password_hash
from .users_admin import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request, redirect


# [update user info]


@ bp.route('/home/update_account', methods=['PATCH'])
@ jwt_required(fresh=True)
def update_user():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)

    lst = {'password', 'email', 'firstname', 'lastname'}
    # [if none of items from lst in json request, return error]
    if all(item not in data for item in lst):
        return jsonify({"error": "Missing a requirement for parsing"})

    # [update firstname]
    if 'firstname' in data:
        if data['firstname'].strip().isalpha() == False:
            return jsonify({"error": "Missing a requirement for parsing"})

        user.firstname = data['firstname'].title().strip()

    # [update last name]
    if 'lastname' in data:
        if data['lastname'].strip().isalpha() == False:
            return jsonify({"error": "Missing a requirement for parsing"})

        user.lastname = data['lastname'].title().strip()

    # [update password]
    if 'password' in data:
        if len(data['password']) < 8:
            return jsonify({"error": "Missing a requirement for parsing"})

        password = data['password'].strip()
        user.password = generate_password_hash(password)

    # [update email]
    if 'email' in data:
        email = data['email'].strip()
        if validate_email(email) == False or validate_email(email) is not None:
            return jsonify({"error": "Incorrect format or email already in use"})

        user.email = email
        user.username = user.email.split('@')[0]

        db.session.commit()

        return redirect('/login')

    try:
        db.session.commit()
        return jsonify(user.serialize())

    except BaseException as error:
        return jsonify({'error': error})
