from flask import Blueprint, jsonify, abort, request, flash
from ..models.models import User, db
from ..commands.commands import confirm_email, check_email
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user


bp = Blueprint('login', __name__, url_prefix='/login')

# Login


@bp.route('', methods=['GET', 'POST'])
def login():
    # Login page
    if request.method == 'GET':
        return 'Login'

    # If neither email, nor password, and remember are used to login, return error
    elif request.method == 'POST' and 'email' not in request.json \
            and ('password' not in request.json and 'remember' not in request.json):
        return abort(400)

    # Either username or email are permitted to sign in, but not both
    elif request.method == 'POST' and 'email' in request.json:
        # check if email exists in db and check if email format is correct
        if check_email(request.json['email'].strip()) == False or confirm_email(request.json['email'].strip().replace(" ", "")) is None:
            return "Invalid email"

        else:
            # Assign either email or username to variable to filter primary key
            user = request.json['email'].strip().replace(" ", "")
            # check if user exists depending on whether username or email were used to sign in
            user_id = db.session.query(User.id).filter(
                User.email == user).first()[0]
            # get user object
            user_obj = User.query.get(user_id)

        password = request.json['password']
        remember = True if request.json['remember'] == 'yes' else False

        # take user supplied password, hash it, and compare it to hashed password in db. Also check if user object was succesfully created
        if not user_obj or not check_password_hash(user_obj.password, password):
            return 'Please check your credentials and try again.'
        # Log user into session
        login_user(user_obj, remember=remember)
        return f'{user_obj.firstname}, logged in Succesfully'

# Logout


@ bp.route('/logout')
@ login_required
def logout():
    logout_user()
    return f'Logged off'
