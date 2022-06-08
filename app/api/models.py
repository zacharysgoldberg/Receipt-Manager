import os
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, make_response, redirect, url_for
from datetime import datetime
import simplejson as json
from sqlalchemy.dialects.postgresql import JSONB
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    get_csrf_token
)


db = SQLAlchemy()

# [user access authorization level]
ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

# User table


class User(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Text, nullable=True)
    lastname = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(200), nullable=False,
                         unique=True, index=True)
    access = db.Column(db.Integer, nullable=False)

    totals_stored = db.relationship(
        'Total', backref='users', cascade='all, delete')
    receipts_stored = db.relationship(
        "Receipt", backref="users", cascade='all, delete')

    #  [contructor for column types]
    def __init__(self, firstname: str, lastname: str, email: str, password: str, username: str, access: int):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.username = username
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access >= access_level

    @staticmethod
    def create_user(email, password, firstname=None, lastname=None, access=1):
        # [add new user]
        user = User(
            email=email,
            password=generate_password_hash(password),
            username=email.split('@')[0],
            firstname=firstname,
            lastname=lastname,
            access=access
        )

        db.session.add(user)
        db.session.commit()

        # [add new total]
        total = Total(
            purchase_totals=0.00,
            tax_totals=0.00,
            tax_year=datetime.now().year,
            user_id=db.session.query(User._id).filter(
                User.email == email).first()[0]
        )

        db.session.add(total)
        db.session.commit()

        return user

    @staticmethod
    def login_user(email, password):
        # [get user object]
        user_id = db.session.query(User._id).filter(
            User.email == email).first()[0]
        user = User.query.get(user_id)
        # [take user supplied password, hash it, and compare it to hashed password in db]
        if not user or not check_password_hash(user.password, password):
            return False
        # [checking if user holds administrator acccess]
        additional_claims = {"is_admin": True if user.allowed(
            ACCESS['admin']) else False}
        # [authenticate with JWT]
        access_token = create_access_token(
            identity=user_id, additional_claims=additional_claims, fresh=True)
        refresh_token = create_refresh_token(user_id)
        # [set the JWTs and the CSRF double submit protection cookies in a response]
        json_resp = jsonify({
            'access_csrf': get_csrf_token(access_token),
            'refresh_csrf': get_csrf_token(refresh_token)
        })
        resp = redirect(url_for('index'))

        # [setting access cookies expiration to 30 minutes]
        set_access_cookies(json_resp, access_token, max_age=1800)
        # [setting refresh cookies expiration to 2 hours]
        set_refresh_cookies(json_resp, refresh_token, max_age=7200)

        return json_resp

    # [serializer returned as a dict/json object]

    def serialize(self):
        return {
            'id': self._id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'username': self.username,
            'access_level': self.access
        }


# Totals table


class Total(db.Model):
    __tablename__ = 'totals'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_totals = db.Column(db.Numeric, nullable=False)
    tax_totals = db.Column(db.Numeric, nullable=False)
    tax_year = db.Column(
        db.BigInteger, default=datetime.year, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=False)

    receipt_totals = db.relationship("Receipt", backref="totals")

    def __init__(self, purchase_totals: float, tax_totals: float, tax_year: str, user_id: int):
        self.purchase_totals = purchase_totals
        self.tax_totals = tax_totals
        self.tax_year = tax_year
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self._id,
            # [Hack to serialize decimal values in JSON !]
            'purchase_totals': json.dumps(self.purchase_totals, use_decimal=True),
            'tax_totals': json.dumps(self.tax_totals, use_decimal=True),
            # [declared year as int type rather than date]
            'tax_year': self.tax_year,
            'user_id': self.user_id
        }


# Receipts table


class Receipt(db.Model):
    __tablename__ = 'receipts'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _from = db.Column(db.Text, nullable=False)
    purchase_total = db.Column(db.Numeric, nullable=False)
    tax = db.Column(db.Numeric, nullable=False)
    address = db.Column(db.Text, nullable=False)
    items_services = db.Column(JSONB, nullable=False, index=True)
    transaction_number = db.Column(db.String(14), nullable=True, unique=True)
    cash = db.Column(db.Boolean, nullable=True)
    card_last_4 = db.Column(db.String(4), nullable=True)
    link = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime,
                          default=datetime,
                          nullable=False)

    total_id = db.Column(db.Integer, db.ForeignKey(
        'totals._id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=False)

    def __init__(self, _from: str, purchase_total: float, tax: float,
                 address: str, transaction_number: str, items_services: list, cash: bool, card_last_4: int, link: str, date_time: str, total_id: int, user_id: int):
        self._from = _from
        self.purchase_total = purchase_total
        self.tax = tax
        self.address = address
        self.transaction_number = transaction_number
        self.items_services = items_services
        self.cash = cash
        self.card_last_4 = card_last_4
        self.link = link
        self.date_time = date_time
        self.total_id = total_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self._id,
            'from': self._from,
            'purchase_total': json.dumps(self.purchase_total, use_decimal=True),
            'tax': json.dumps(self.tax, use_decimal=True),
            'address': self.address,
            'transaction_number': self.transaction_number,
            'items_services': self.items_services,
            'cash': self.cash,
            'card_last_4': self.card_last_4,
            'link': self.link,
            'date_time': self.date_time,
            'total_id': self.total_id,
            'user_id': self.user_id
        }
