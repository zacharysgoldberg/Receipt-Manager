import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from decouple import config

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # SQLALCHEMY_DATABASE_URI='postgresql://postgres:admin123@primary.caf07lihg7ag.us-west-1.rds.amazonaws.com:5432/receipt_manager',
        # Using protected env varaibles for URI
        SQLALCHEMY_DATABASE_URI=f"postgresql://{config('USER')}:{config('PASSWORD')}@localhost:5432/{config('DB')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    # Initialize flask login manager
    login_manager = LoginManager()
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

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

    from .models.models import db, User
    db.init_app(app)
    migrate = Migrate(app, db)

    from .views import login, users, receipts, totals
    app.register_blueprint(login.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(receipts.bp)
    app.register_blueprint(totals.bp)

    # To query for the user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
