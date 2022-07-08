import os
from .models import db
# from .blocklist import jwt_redis_blocklist
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv


# [plugins]
mail = Mail()
jwt = JWTManager()
load = load_dotenv()

# [app factory]


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY'),
        # [development URI]
        # SQLALCHEMY_DATABASE_URI=os.getenv('DEVELOPMENT_DB'),
        # [Heroku URI]
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        JWT_TOKEN_LOCATION=['cookies', 'headers'],
        JWT_COOKIE_SECURE=False,    # [True for production]
        JWT_ACCESS_COOKIE_PATH='/users',
        JWT_REFRESH_COOKIE_PATH='/login/refresh',
        JWT_COOKIE_CSRF_PROTECT=True,
        JWT_CSRF_CHECK_FORM=True,
        JWT_ACCESS_CSRF_HEADER_NAME="X-CSRF-TOKEN-ACCESS",
        JWT_REFRESH_CSRF_HEADER_NAME="X-CSRF-TOKEN-REFRESH",
        MAIL_SERVER='smtp.mailgun.org',
        MAIL_PORT=587,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_USE_TLS=True,
        # UPLOAD_PATH='app/api/receipts/images'
    )

    # [initialize plugins]
    jwt.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    # [JWT error handling decorators]

    @ jwt.expired_token_loader
    def expired_token_callback(decrypted_header, decrypted_token):
        return jsonify({
            'description': "The token has expired",
            'error': 'token_expired'
        }), 401

    @ jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401

    @ jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain an access token',
            'error': 'authorization_required'
        })

    @ jwt.needs_fresh_token_loader
    def token_not_fresh_callback(decrypted_header, decrypted_token):
        return jsonify({
            'description': 'The token is not fresh',
            'error': 'fresh_token_required'
        })

    @ jwt.revoked_token_loader
    def revoked_token_callback(decrypted_header, decrypted_token):
        return jsonify({
            'description': 'The token has been revoked',
            'error': 'token_revoked'
        })

    # [initialize blueprint endpoints]
    from .totals import totals_admin, get_totals
    from .receipts import add_receipt, update_receipt, remove_receipt, receipts_admin
    from .login import login, logout, refresh, register, reset_password
    from .users import update_user, users_admin, delete_account

    app.register_blueprint(users_admin.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(receipts_admin.bp)
    app.register_blueprint(totals_admin.bp)

    return app
