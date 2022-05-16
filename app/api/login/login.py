from ..commands.validate import validate_email
from ..models import User, db
from datetime import datetime
from flask import(
    Blueprint,
    jsonify,
    abort,
    request,
    redirect,
    render_template,
    url_for
)
from flask_jwt_extended import get_jwt


bp = Blueprint('login', __name__, url_prefix='/login')

# [login]


@ bp.route('', methods=['GET', 'POST'])
def login():
    # [login page]
    if request.method == 'GET':
        return render_template('login.html')

    # [if neither email, nor password, and remember are used to login, return error]
    elif request.method == 'POST':
        # if 'email' not in request.json \
        #         and 'password' not in request.json:
        #     return abort(400)

        email = request.form.get('email')
        # email = request.json['email']

        # [check if email exists in db and check if email format is correct]
        if validate_email(email) is None or validate_email(email) == False:
            return jsonify({'message': 'Invalid email. Please try again'})

        password = request.form.get('password')
        # password = request.json['password']

        # [login user and return response]
        login_user = User.login_user(email, password)

        if login_user:
            result = [bill for bill in login_user.bills_stored]
            if result:
                for bill in result:
                    if datetime.now() > bill.due_date:
                        bill.past_due = True
                        db.session.commit()

            return redirect(url_for('home.index'))

        return render_template('login.html')
