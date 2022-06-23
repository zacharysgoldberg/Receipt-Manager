from flask import jsonify, redirect, url_for
from flask_jwt_extended import (create_access_token, get_jwt_identity,
                                jwt_required, set_access_cookies)
from .login import bp

# [refresh token]


@ bp.route('/refresh', methods=['POST'])
@ jwt_required(refresh=True)
def token_refresh():
    # [get user by jwt identity payload (id)]
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)
    # [set the access JWT and CSRF double submit protection cookies in a response]
    resp = redirect(url_for('index'))
    set_access_cookies(resp, new_token, max_age=1800)   # 30 minutes

    return resp
