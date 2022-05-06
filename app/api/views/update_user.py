from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import confirm_email, check_email
from werkzeug.security import generate_password_hash
from flask_login import login_required, logout_user, current_user
from .login import bp

# Update

# Update user info


@ bp.route('/logged_in/<username>', methods=['PATCH'])
@ login_required
def update_user(username: str):
    data = request.get_json()

    user_id = db.session.query(User.id).filter(
        User.username == username).first()[0]
    user = User.query.get_or_404(user_id)
    lst = ['password', 'email', 'firstname', 'lastname']

    # If none of items from lst in json request, return error
    if all(item not in data for item in lst):
        return abort(400)
    # Update firstname
    if 'firstname' in data:
        if data['firstname'].strip().isalpha() == False:
            return abort(400)
        user.firstname = data['firstname'].title().strip()
    # Update last name
    if 'lastname' in data:
        if data['lastname'].strip().isalpha() == False:
            return abort(400)
        user.lastname = data['lastname'].title().strip()
    # Update password
    if 'password' in data:
        if len(data['password']) < 8:
            return abort(400)
        password = data['password'].strip().replace(" ", "")
        user.password = generate_password_hash(password)
    # update email
    if 'email' in data:
        email = data['email'].strip().replace(" ", "")
        if check_email(email) == False or confirm_email(email) is not None:
            return abort(400)
        user.email = email
        user.username = user.email.split('@')[0]
        user = current_user
        user.authenticated = False
        db.session.commit()
        logout_user()
        return redirect('/login')

    try:
        db.session.commit()
        return jsonify(user.serialize())

    except:
        return jsonify(False)
