from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import User, db
from ..commands.commands import confirm_email, check_email
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


bp = Blueprint('login', __name__, url_prefix='/login')

# Login


@bp.route('', methods=['GET', 'POST'])
def login():
    # Login page
    if request.method == 'GET':
        return 'Login'

    # If neither email, nor password, and remember are used to login, return error
    elif request.method == 'POST' and 'email' not in request.json \
            and 'password' not in request.json and 'remember' not in request.json:
        return abort(400)

    else:
        # check if email exists in db and check if email format is correct
        email = request.json['email'].strip().replace(" ", "")
        print(email)
        if check_email(email) == False or confirm_email(email) is None:
            return "Invalid email"
        # Assign email to variable for filtering primary key
        # check if user exists using email
        user_id = db.session.query(User.id).filter(
            User.email == email).first()[0]
        # get user object
        user = User.query.get(user_id)
        if len(request.json['password']) < 8:
            return 'Password must be at least 8 characters'
        # Assign password to var for checking against db
        password = request.json['password']
        if type(request.json['remember']) != bool:
            return 'Remember me must be set to True or False'
        # Assign remember login cred. to var
        remember = request.json['remember']

        # take user supplied password, hash it, and compare it to hashed password in db. Also check if user object was succesfully created
        if not user or not check_password_hash(user.password, password):
            return 'Please check your credentials and try again.'
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        # Log user into session
        login_user(user, remember=remember)
        return f'{user.firstname}, logged in Succesfully'


# Logout


@ bp.route('/logged_out')
@ login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/login')
