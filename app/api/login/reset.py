import os
from api import mail, load
from flask_mail import Message
from ..commands.validate import validate_email
from ..models import User, db
from .login import bp
from flask import(
    Blueprint,
    jsonify,
    abort,
    request,
    redirect,
    render_template,
    url_for
)
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    set_refresh_cookies,
)


def send_email(email):
    user_id = db.session.query(User._id).filter(
        User.email == email).first()[0]
    user = User.query.get(user_id)

    new_token = create_access_token(identity=user, fresh=False)

    msg = Message()
    msg.subject = "Stub-Manager Password Reset"
    msg.sender = os.getenv('ADMIN')
    msg.recipients = [user.email]
    msg.html = render_template('reset_email.html', user=user, token=new_token)

    mail.send(msg)


@bp.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'GET':
        return render_template('reset_email.html')

    if request.method == 'POST':

        email = request.form.get('email')
        if validate_email(email) is None or validate_email(email) == False:
            return jsonify({'message': 'Invalid email. Please try again'})

        else:
            send_email(email)

        return redirect(url_for('login.html'))
