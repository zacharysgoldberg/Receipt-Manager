from ..commands.validate import validate_email
from ..models import User, db
from datetime import datetime
from flask import Blueprint, jsonify, request


bp = Blueprint('login', __name__, url_prefix='/login')

# [login]


@ bp.route('', methods=['GET', 'POST'])
def login():
    # [login page]
    if request.method == 'GET':
        return "Login"

    elif request.method == 'POST':
        email = request.json['email']

        # [check if email exists in db and check if email format is correct]
        if validate_email(email) is None or validate_email(email) == False:
            return jsonify({'error': 'Invalid email. Please try again'})

        password = request.json['password']

        # [login user and return response]
        login_user, resp = User.login_user(email, password)

        if login_user and resp:
            return resp

        return jsonify({'error': 'Invalid Credentials'})
