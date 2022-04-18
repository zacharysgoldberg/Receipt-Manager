from flask import Blueprint, jsonify, abort, request, flash
from ..models.models import User, db
from ..commands.commands import confirm_user, check_email
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user


bp = Blueprint('login', __name__, url_prefix='/login')


@bp.route('', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'Login'

    elif request.method == 'POST' and 'email' not in request.json:
        return abort(400)

    elif request.method == 'POST' and 'email' in request.json:
        if check_email(request.json['email']) == False:
            return "Invalid email"

        email = request.json['email']
        password = request.json['password']
        remember = True if request.json['remember'] == 'yes' else False

        # check if the user exists
        user_id = db.session.query(User.id).filter(
            User.email == email).first()[0]
        user = User.query.get(user_id)

        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            return 'Please check your credentials and try again.'

        login_user(user, remember=remember)
        return f'{user.firstname}, logged in Succesfully'


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return f'Logged off'
