import datetime
from ..commands.validate import validate_email
from ..models import User, db
from .login import bp
from ..commands.send_email import send_email
from flask_jwt_extended import create_access_token
from flask import(
    jsonify,
    request,
    render_template,
)


@bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return "Forgot Password"

    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data['email']
            if not email:
                return jsonify({"error": "Please enter the email associated with the account"})
            user_id = db.session.query(User._id).filter(
                User.email == email).first()[0]
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "Email does not exist"})

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(
                str(user_id), expires_delta=expires)

            send_email(subject='[Stub-Manager] Reset Your Password',
                       sender='zachgoldberg29@gmail.com',
                       recipients=[user.email],
                       text=render_template('reset_password.txt',
                                            url=request.host_url + 'login/forgot_password/' + reset_token))
            return jsonify({'message': f"A link has been sent to {user.email}"})

        except TypeError as error:
            raise jsonify({'error': error})

        except ValueError as error:
            raise jsonify({'error': error})


@ bp.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')

    if request.method == 'POST':
        email = request.json['email']

        if validate_email(email) == False:
            return jsonify({'error': 'Invalid email. Please try again'})

        # send_email(email)

        return jsonify({"message": f"Password has been reset for {email}"})
