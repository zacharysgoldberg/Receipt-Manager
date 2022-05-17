from ..commands.validate import validate_email
from ..models import User, db
from datetime import datetime
from flask import(
    Blueprint,
    jsonify,
    request,
    redirect
)
from flask_jwt_extended import get_jwt


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
            result = [bill for bill in login_user.bills_stored]
            if result:
                for bill in result:
                    if datetime.now() > bill.due_date:
                        bill.past_due = True
                        db.session.commit()

            return resp
