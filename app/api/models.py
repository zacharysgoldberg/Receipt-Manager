from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime
import simplejson as json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    get_csrf_token
)


db = SQLAlchemy()


# User table


class User(db.Model):
    __tablename__ = 'users'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(200), nullable=False,
                         unique=True, index=True)

    totals_stored = db.relationship(
        'Total', backref='users', cascade='all, delete')
    receipts_stored = db.relationship(
        "Receipt", backref="users", cascade='all, delete')
    bills_stored = db.relationship(
        'Bill', backref='users', cascade='all, delete')

    #  [contructor for column types]
    def __init__(self, firstname: str, lastname: str, email: str, password: str, username: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.username = username

    @staticmethod
    def create_user(firstname, lastname, email, password, username):
        # [add new user]
        user = User(
            firstname=firstname,
            lastname=lastname,
            password=generate_password_hash(password),
            email=email,
            username=username
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
            return False  # jsonify({'message': 'Invalid Credentials'})

        # [authenticate with JWT]
        access_token = create_access_token(identity=user_id, fresh=True)
        refresh_token = create_refresh_token(user_id)
        # [set the JWTs and the CSRF double submit protection cookies in a response]
        resp = jsonify({
            'access_csrf': get_csrf_token(access_token),
            'refresh_csrf': get_csrf_token(refresh_token)
        })
        # [setting access cookies expiration to 30 minutes]
        set_access_cookies(resp, access_token, max_age=1800)
        # [setting refresh cookies expiration to 2 hours]
        set_refresh_cookies(resp, refresh_token, max_age=7200)

        return user  # resp, user

    # [serializer returned as a dict/json object]

    def serialize(self):
        return {
            'id': self._id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'username': self.username
        }


# Totals table

class Total(db.Model):
    __tablename__ = 'totals'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_totals = db.Column(db.Numeric, nullable=False)
    tax_totals = db.Column(db.Numeric, nullable=False)
    tax_year = db.Column(
        db.BigInteger, default=datetime.year, nullable=False)
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
    purchase_total = db.Column(db.Numeric, nullable=False)
    tax = db.Column(db.Numeric, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    transaction_number = db.Column(db.String(14), nullable=True, unique=True)
    description = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime,
                          default=datetime,
                          nullable=False)

    total_id = db.Column(db.Integer, db.ForeignKey(
        'totals._id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=False)

    def __init__(self, purchase_total: float, tax: float,
                 city: str, state: str, transaction_number: str, description: str, date_time: str, total_id: int, user_id: int):
        self.purchase_total = purchase_total
        self.tax = tax
        self.city = city
        self.state = state
        self.transaction_number = transaction_number
        self.description = description
        self.date_time = date_time
        self.total_id = total_id
        self.user_id = user_id

    @staticmethod
    def add_receipt(
        purchase_total, tax, city,
        state, transaction_number, description,
        date_time, total_id, user_id
    ):
        # [add new receipt for existing tax year]
        receipt = Receipt(
            purchase_total=purchase_total,
            tax=tax,
            city=city,
            state=state,
            transaction_number=transaction_number,
            description=description,
            date_time=date_time,
            total_id=total_id,
            user_id=user_id
        )

        db.session.add(receipt)
        db.session.commit()

        return receipt

    def serialize(self):
        return {
            'id': self._id,
            'purchase_total': json.dumps(self.purchase_total, use_decimal=True),
            'tax': json.dumps(self.tax, use_decimal=True),
            'city': self.city,
            'state': self.state,
            'transaction_number': self.transaction_number,
            'description': self.description,
            'date_time': self.date_time,
            'total_id': self.total_id,
            'user_id': self.user_id
        }


class Bill(db.Model):
    __tablename__ = 'bills'
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    issuer = db.Column(db.Text, nullable=False)
    balance = db.Column(db.Numeric, nullable=False)
    date_of_issue = db.Column(
        db.DateTime, default=datetime.date, nullable=False)
    amount_due = db.Column(db.Numeric, nullable=False)
    fees = db.Column(db.Numeric, nullable=True)
    interest = db.Column(db.Numeric, nullable=True)
    due_date = db.Column(db.DateTime, default=datetime.date, nullable=False)
    invoice_number = db.Column(db.BigInteger, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    paid = db.Column(db.Boolean, nullable=False)
    past_due = db.Column(db.Boolean, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users._id'), nullable=False)

    def __init__(
        self, issuer: str, balance: float, date_of_issue: str,
        amount_due: float, fees: float, interest: float, due_date: str,
        invoice_number: int, description: str, paid: bool, past_due: bool,
        user_id: int
    ):
        self.issuer = issuer
        self.balance = balance
        self.date_of_issue = date_of_issue
        self.amount_due = amount_due
        self.fees = fees
        self.interest = interest
        self.due_date = due_date
        self.invoice_number = invoice_number
        self.description = description
        self.paid = paid
        self.past_due = past_due
        self.user_id = user_id

    @staticmethod
    def add_bill(
        issuer, balance, date_of_issue, amount_due,
        fees, interest, due_date, invoice_number,
        descripton, paid, past_due, user_id
    ):

        bill = Bill(
            issuer=issuer,
            balance=balance,
            date_of_issue=date_of_issue,
            amount_due=amount_due,
            fees=fees,
            interest=interest,
            due_date=due_date,
            invoice_number=invoice_number,
            description=descripton,
            paid=paid,
            past_due=past_due,
            user_id=user_id
        )

        db.session.add(bill)
        db.session.commit()

        return bill

    def serialize(self):
        return {
            "id": self._id,
            "issuer": self.issuer,
            "balance": self.balance,
            "date_of_issue": self.date_of_issue,
            "amount_due": self.amount_due,
            "fees": self.fees,
            "interest": self.interest,
            "due_date": self.due_date,
            "invoice_number": self.invoice_number,
            "description": self.description,
            "paid": self.paid,
            "past_due": self.past_due,
            "user_id": self.user_id
        }
