# from ..blocklist import jwt_redis_blocklist, ACCESS_EXPIRES
from ..users.get_users import bp
from flask import(
    Blueprint,
    jsonify,
    abort,
    request,
    redirect
)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
    unset_jwt_cookies,
    # unset_access_cookies,
)

# [logout]


@ bp.route('/logged_out', methods=['POST'])
def logout():
    # [(JWT ID)]
    # jti = get_jwt()['jti']
    # [add token to redis blocklist upon logout]
    # jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)

    resp = jsonify({'logout': True})
    # [send a response to delete the cookies in order to logout]
    unset_jwt_cookies(resp)

    return resp
