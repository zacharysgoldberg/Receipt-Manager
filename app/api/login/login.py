from ..commands.validate import validate_email
from ..models import User, db
from datetime import datetime
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import get_jwt_identity, get_jwt


bp = Blueprint('login', __name__, url_prefix='/login')

# [login]


@ bp.route('', methods=['GET', 'POST'])
def login():
    # [login page]
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        email = request.form['email']

        # [check if email exists in db and check if email format is correct]
        if validate_email(email) is None or validate_email(email) == False:
            return jsonify({'error': 'Invalid email. Please try again'})

        password = request.form['password']

        # [login user and return response]
        resp = User.login_user(email, password)

        if resp:
            return resp

        return jsonify({'error': 'Invalid Credentials'})
