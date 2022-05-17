import os
import datetime
from ..commands.validate import validate_email
from ..models import User, db
from ..commands.send_email import send_email
from .login import bp
from flask import(
    jsonify,
    request,
    redirect,
    render_template,
    url_for
)
from flask_jwt_extended import create_access_token


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return "Forgot Password"

    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            if not email:
                return jsonify({"message": "Please enter email"})
            user_id = db.session.query(User._id).filter(
                User.email == email).first()[0]
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "Email does not exist"})

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(
                str(user_id), expires_delta=expires)

            send_email(subject='[Stub-Manager] Reset Your Password',
                       sender='zachgoldberg29@gmail.com',
                       recipients=[user.email],
                       text=render_template('reset_password.txt',
                                            url=request.host_url + 'login/forgot_password/' + reset_token))
            return jsonify({'message': f"A email containing a link to reset your password has been sent to '{user.email}'"})

        except TypeError as error:
            raise jsonify({'error': error})
        except ValueError as error:
            raise jsonify({'error': error})


@ bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return "Reset Password"  # render_template('reset_email.html')

    if request.method == 'POST':

        email = request.json['email']
        if validate_email(email) == False:
            return jsonify({'message': 'Invalid email. Please try again'})

        send_email(email)
        # redirect(url_for('login.html'))
        return jsonify({"message": f"Sent password reset to {email}"})
