from flask import Blueprint, jsonify, abort, request, render_template
from ..models import Total, User, db
from ..commands.validate import validate_email
from .login import bp

# [create a user]


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return "Register"  # render_template('register.html')

    elif request.method == 'POST':
        lst = {'password', 'firstname', 'lastname', 'email'}
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

        firstname = data['firstname'].capitalize().strip()
        lastname = data['lastname'].capitalize().strip()
        email = data['email'].strip()
        password = data['password']
        username = email.split('@')[0]

        # [add new user]
        new_user = User.create_user(
            firstname, lastname, email, password, username)

        return jsonify(new_user.serialize())
