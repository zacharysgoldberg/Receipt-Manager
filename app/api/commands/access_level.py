from functools import wraps
from flask import jsonify, redirect, request, url_for
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from ..models import User, db

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
