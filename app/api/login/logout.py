# from ..blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from ..users.users_admin import bp
from flask import jsonify, redirect, url_for, make_response
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    # get_jwt,
    # unset_access_cookies,
    unset_jwt_cookies
)


# [logout]


@bp.route('/logged_out', methods=['GET'])
@jwt_required()
def logout():
    # [(JWT ID)]
    # jti = get_jwt()['jti']
    # [add token to redis blocklist upon logout]
    # jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    resp = redirect(url_for('login.login'))
    json_resp = jsonify({'logged out': True})
    # [send a response to delete the cookies in order to logout]
    unset_jwt_cookies(resp)

    return json_resp
