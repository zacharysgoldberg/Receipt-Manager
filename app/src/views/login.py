from flask import Blueprint, jsonify, abort, request, flash
from ..models.models import User, db
from ..commands.commands import confirm_user, check_email
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user


bp = Blueprint('login', __name__, url_prefix='/login')

# Login


@bp.route('', methods=['GET', 'POST'])
def login():
    # Login page
    if request.method == 'GET':
        return 'Login'
    # If neither username, email, nor password, and remember are used to login, return error
    elif request.method == 'POST' \
            and ('username' not in request.json or 'email' not in request.json) \
            and ('password' not in request.json and 'remember' not in request.json):
        return abort(400)
    # If both username and email are used to login, return error
    elif request.method == 'POST' \
            and ('email' in request.json and 'username' in request.json):
        return abort(400)
    # Either username or email are permitted to sign in, but not both
    elif request.method == 'POST' \
            and ('email' in request.json or 'username' in request.json):
        # If email is used, check if format is correct
        if 'username' not in request.json and check_email(request.json['email'].strip()) == False:
            return "Invalid email"
        # If username is used, check if it exists
        elif 'email' not in request.json \
                and confirm_user(request.json['username'].strip().replace(" ", "")) is None:
            return 'Invalid username'

        else:
            # Assign either email or username to variable to filter primary key
            user = request.json['email'] if 'email' in request.json else request.json['username']
            # check if user exists depending on whether username or email were used to sign in
            user_id = db.session.query(User.id).filter(
                User.email == user).first()[0] if 'email' in request.json \
                else db.session.query(User.id).filter(
                User.username == user).first()[0]
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
