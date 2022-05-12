from flask import Flask, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from .blocklist import jwt_redis_blocklist
import os
import redis


# using dotenv to retrieve .env variables
load_dotenv()

# app factory


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Using protected env varaibles
        # JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
        SECRET_KEY=os.getenv('SECRET_KEY'),
        # Development URI
        # SQLALCHEMY_DATABASE_URI=f"postgresql://postgres@localhost/{os.getenv('POSTGRES_DB')}",
        # Heroku URI
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URI'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        PROPAGATE_EXCEPTIONS=True
    )

    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == os.environ['ADMIN']:
            return {'is_admin': True}
        return {'is_admin': False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(decrypted_header, decrypted_token):
        token_in_redis = jwt_redis_blocklist.get(decrypted_token['jti'])
        return token_in_redis is not None

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

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import (
        users, login, create_receipt, read_login,
        update_receipt, update_user, delete, receipts, totals
    )
    app.register_blueprint(users.bp)
    app.register_blueprint(login.bp)
    app.register_blueprint(receipts.bp)
    app.register_blueprint(totals.bp)

    return app
