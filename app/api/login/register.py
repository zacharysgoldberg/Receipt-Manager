from flask import jsonify, redirect, render_template, request, url_for
from ..commands.validate import validate_email
from ..models import User
from .login import bp

# [create a user]


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
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

        # [add new user]
        new_user = User.create_user(
            email, password
        )

        resp = redirect(url_for("login.login"))
        json_resp = jsonify(new_user.serialize())

        if new_user:
            return resp
