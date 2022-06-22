# from ..blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from flask import jsonify, make_response, redirect, url_for
from flask_jwt_extended import (get_jwt_identity, jwt_required,
                                unset_jwt_cookies)
from ..users.users_admin import bp

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
