from flask import(
    Blueprint,
    jsonify,
    abort,
    request,
    redirect
)
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import check_password_hash
from ..commands.security import check_email
from ..models.models import User, db
from ..blocklist import BLOCKLIST


bp = Blueprint('login', __name__, url_prefix='/login')


# Login
@bp.route('', methods=['GET', 'POST'])
def login():
    # Login page
    if request.method == 'GET':
        return 'Login'

    # If neither email, nor password, and remember are used to login, return error
    elif request.method == 'POST' and 'email' not in request.json \
            and 'password' not in request.json:
        return abort(400)

    else:
        data = request.get_json()
        # check if email exists in db and check if email format is correct
        email = data['email'].strip().replace(" ", "")

        if check_email(email) == False:     # or confirm_email(email) is None
            return jsonify({'message': 'Invalid email format'})
        # check if user exists using email
        user_id = db.session.query(User.id).filter(
            User.email == email).first()[0]
        # get user object
        user = User.query.get(user_id)
        # Assign password to var for checking against db
        password = data['password']
        # take user supplied password, hash it, and compare it to hashed password in db. Also check if user object was succesfully created
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid Credentials'})
        # Authenticate with JWT
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(user_id)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })


# Refresh token


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def token_refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({'access_token': new_token})

# Logout


@ bp.route('/logged_out', methods=['POST'])
@jwt_required()
def logout():
    # jti (JWT ID)
    jti = get_jwt()['jti']
    # Add token to blocklist set
    BLOCKLIST.add(jti)
    return redirect('/login')
