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
from ..commands.validate import validate_email
from ..models.models import User, db
from ..blocklist import jwt_redis_blocklist, ACCESS_EXPIRES

bp = Blueprint('login', __name__, url_prefix='/login')


# [login]
@bp.route('', methods=['GET', 'POST'])
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
        user_id = db.session.query(User.id).filter(
            User.email == email).first()[0]
        user = User.query.get(user_id)
        # [take user supplied password, hash it, and compare it to hashed password in db. Also check if user object was succesfully created]
        password = data['password']
        if not user or not check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid Credentials'})
        # [authenticate with JWT]
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(user_id)

        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        })


# [refresh token]


@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def token_refresh():
    # [get user by jwt identity payload (id)]
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({'access_token': new_token})

# [logout]


@ bp.route('/logged_out', methods=['POST'])
@jwt_required()
def logout():
    # [(JWT ID)]
    jti = get_jwt()['jti']
    # [add token to redis blocklist upon logout]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return redirect('/login')
