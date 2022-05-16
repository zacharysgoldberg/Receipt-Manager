from werkzeug.security import check_password_hash
from ..commands.validate import validate_email
from ..models import User, db
from datetime import datetime
from flask import(
    Blueprint,
    jsonify,
    abort,
    request,
    redirect
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    get_csrf_token
)

bp = Blueprint('login', __name__, url_prefix='/login')

# [login]


@ bp.route('', methods=['GET', 'POST'])
def login():
    # [login page]
    if request.method == 'GET':
        return 'Login'

    # [if neither email, nor password, and remember are used to login, return error]
    elif request.method == 'POST' and 'email' not in request.json \
            and 'password' not in request.json:
        return abort(400)

    else:
        data = request.get_json()
        # [check if email exists in db and check if email format is correct]
        email = data['email'].strip().replace(" ", "")

        if validate_email(email) is None or validate_email(email) == False:
            return jsonify({'message': 'Invalid email. Please try again'})

        # [get user object]
        user_id = db.session.query(User._id).filter(
            User.email == email).first()[0]
        user = User.query.get(user_id)
        # [take user supplied password, hash it, and compare it to hashed password in db]
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid Credentials'})

        # [authenticate with JWT]
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(user_id)
        # [set the JWTs and the CSRF double submit protection cookies in a response]
        resp = jsonify({
            'access_csrf': get_csrf_token(access_token),
            'refresh_csrf': get_csrf_token(refresh_token)
        })
        # [setting access cookies expiration to 30 minutes]
        set_access_cookies(resp, access_token, max_age=1800)
        # [setting refresh cookies expiration to 2 hours]
        set_refresh_cookies(resp, refresh_token, max_age=7200)

        result = [bill for bill in user.bills_stored]

        if result:

            for bill in result:

                if datetime.now() > bill.due_date:
                    bill.past_due = True
                    db.session.commit()

        return resp
