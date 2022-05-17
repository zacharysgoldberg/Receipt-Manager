from .login import bp
from flask import jsonify, redirect
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies
)

# [refresh token]


@ bp.route('/refresh', methods=['POST'])
@ jwt_required(refresh=True)
def token_refresh():
    # [get user by jwt identity payload (id)]
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    # [set the access JWT and CSRF double submit protection cookies in a response]
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, new_token, max_age=1800)   # 30 minutes

    return resp
