import os
from .models import db
# from .blocklist import jwt_redis_blocklist
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load = load_dotenv()
mail = Mail()
jwt = JWTManager()

# [app factory]


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        # [using protected env varaibles]
        SECRET_KEY=os.getenv('SECRET_KEY'),
        # [development URI]
        SQLALCHEMY_DATABASE_URI=f"postgresql://postgres@localhost/{os.getenv('POSTGRES_DB')}",
        # [Heroku URI]
        # SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        JWT_TOKEN_LOCATION=['cookies'],
        JWT_COOKIE_SECURE=False,    # [True for production]
        JWT_ACCESS_COOKIE_PATH='/home/',
        JWT_REFRESH_COOKIE_PATH='/login/refresh',
        JWT_COOKIE_CSRF_PROTECT=True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
        MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
        MAIL_USE_TSL=False,
        MAIL_USE_SSL=True
    )

    jwt.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == os.getenv('ADMIN'):
            return {'is_admin': True}
        return {'is_admin': False}

    # [check if refresh token was revoked (Redis)]
    # @jwt.token_in_blocklist_loader
    # def check_if_token_in_blocklist(decrypted_header, decrypted_token):
    #     token_in_redis = jwt_redis_blocklist.get(decrypted_token['jti'])
    #     return token_in_redis is not None

    @jwt.expired_token_loader
    def expired_token_callback(decrypted_header, decrypted_token):
        return jsonify({
            'description': "The token has expired",
            'error': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'description': 'Signature verification failed',
            'error': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'description': 'Request does not contain an access token',
            'error': 'authorization_required'
        })

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(decrypted_header, decrypted_token):
        return jsonify({
            'description': 'The token is not fresh',
            'error': 'fresh_token_required'
        })

    @jwt.revoked_token_loader
    def revoked_token_callback(decrypted_header, decrypted_token):
        return jsonify({
            'description': 'The token has been revoked',
            'error': 'token_revoked'
        })

    from .totals import totals
    from .receipts import receipts, add_receipt
    from .bills import add_bill, get_delete_bill
    from .login import login, logout, refresh, register, home_page, reset_password
    from .users import (
        get_users,
        get_receipts_totals,
        delete_receipt_user,
        update_receipt,
        update_user
    )

    app.register_blueprint(home_page.bp)
    app.register_blueprint(get_users.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(receipts.bp)
    app.register_blueprint(totals.bp)

    return app
