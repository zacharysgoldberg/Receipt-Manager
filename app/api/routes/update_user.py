from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import confirm_email, check_email
from werkzeug.security import generate_password_hash
from flask_login import login_required
from .login import bp

# Update

# Update user info


@ bp.route('/logged_in/<int:id>', methods=['PATCH'])
@ login_required
def update_user(id: int):
    user = User.query.get_or_404(id)
    lst = ['password', 'email', 'firstname', 'lastname']

    # If none of items from lst in json request, return error
    if all(item not in request.json for item in lst):
        return abort(400)
    # Update firstname
    if 'firstname' in request.json:
        if request.json['firstname'].strip().isalpha() == False:
            return abort(400)
        user.firstname = request.json['firstname'].title().strip()
    # Update last name
    if 'lastname' in request.json:
        if request.json['lastname'].strip().isalpha() == False:
            return abort(400)
        user.lastname = request.json['lastname'].title().strip()
    # Update password
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        password = request.json['password'].strip().replace(" ", "")
        user.password = generate_password_hash(password)
    # update email
    if 'email' in request.json:
        email = request.json['email'].strip().repalce(" ", "")
        if check_email(email) == False or confirm_email(email) is not None:
            return abort(400)
        user.email = email

    try:
        db.session.commit()
        return jsonify(user.serialize())

    except:
        return jsonify(False)
