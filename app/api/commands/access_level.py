from functools import wraps
from flask import url_for, request, redirect, jsonify
from ..models import User, db
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# [decorator to require administrator access for protected endpoints]


def admin_required():
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            # [ensure current user in request is an administrator]
            if claims["is_admin"]:
                return f(*args, **kwargs)

            return jsonify(message="Reserved for administrator access"), 403

        return decorator

    return wrapper
