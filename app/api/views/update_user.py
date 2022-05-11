from flask import (
    jsonify,
    abort,
    request,
    redirect
)
from ..models.models import User, db
from ..commands.security import check_email, validate_email
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from .users import bp

# Update

# Update user info


@ bp.route('/update_account', methods=['PATCH'])
@ jwt_required(fresh=True)
def update_user():
    data = request.get_json()

    user_id = get_jwt_identity()
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
        if check_email(email) == False or validate_email(email) is not None:
            return jsonify({"message": "Incorrect format or email already in use"})
        user.email = email
        user.username = user.email.split('@')[0]

        db.session.commit()

        return redirect('/login')

    try:
        db.session.commit()
        return jsonify(user.serialize())

    except:
        return jsonify({'error': 'Unable to fullfil request'})
