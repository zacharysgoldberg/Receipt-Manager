from flask import jsonify, request, render_template, redirect, url_for
from ..models import User
from ..commands.validate import validate_email
from .login import bp

# [create a user]


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        # data = request.get_json()
        # [ensure password is at least 8 characters in length]
        if len(request.form['password']) < 8:
            return jsonify({"error": "Password must be at least 8 characters"})

        email = request.form['email'].strip().replace(" ", "")
        # [check if email exists in db]
        if validate_email(email) is not None:
            return jsonify({'error': 'Email is already in use'})
        # [checking email is in a valid format]
        elif validate_email(email) == False:
            return jsonify({'error': 'Email format is incorrect'})

        # firstname = request.form['firstname'].capitalize().strip()
        # lastname = request.form['lastname'].capitalize().strip()
        email = request.form['email'].strip()
        password = request.form['password']
        username = email.split('@')[0]

        # [add new user]
        User.create_user(
            email, password, username
        )

        # jsonify(new_user.serialize())
        return redirect(url_for('login.login'))
