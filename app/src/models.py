from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import simplejson as json
from decimal import Decimal

db = SQLAlchemy()


# many-to-many tables


users_receipts = db.Table(
    'users_receipts',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),

    db.Column('receipt_id',
              db.Integer,
              db.ForeignKey('receipts.id'),
              primary_key=True),

)


users_totals = db.Table(
    'users_totals',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),

    db.Column('total_id',
              db.Integer,
              db.ForeignKey('totals.id'),
              primary_key=True),

)

# User table


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(128), nullable=False,
                         unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)

    totals = db.relationship(
        'Total', secondary=users_totals, backref='users')
    receipts = db.relationship(
        'Receipt', secondary=users_receipts, backref='users')

    def __init__(self, firstname: str, lastname: str, username: str,
                 password: str,
                 email: str):
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.password = password
        self.email = email

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email
        }


receipts_totals = db.Table(
    'receipts_totals',
    db.Column('receipt_id',
              db.Integer,
              db.ForeignKey('receipts.id'),
              primary_key=True),

    db.Column('total_id',
              db.Integer,
              db.ForeignKey('totals.id'),
              primary_key=True)
)

# Totals table


class Total(db.Model):
    __tablename__ = 'totals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_totals = db.Column(db.Numeric, nullable=False)
    tax_totals = db.Column(db.Numeric, nullable=False)
    tax_year = db.Column(
        db.BigInteger, default=datetime.year, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    receipts = db.relationship("Receipt", secondary=receipts_totals,
                               backref="totals")

    def __init__(self, purchase_totals: float, tax_totals: float, tax_year: str, user_id: int):
        self.purchase_totals = purchase_totals
        self.tax_totals = tax_totals
        self.tax_year = tax_year
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            # Hack to serialize decimal values in JSON !
            'purchase_totals': json.dumps(self.purchase_totals, use_decimal=True),
            'tax_totals': json.dumps(self.tax_totals, use_decimal=True),
            # Declared year as int type rather than date
            'tax_year': self.tax_year,
            'user_id': self.user_id
        }


# Receipts table


class Receipt(db.Model):
    __tablename__ = 'receipts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    purchase_total = db.Column(db.Numeric, nullable=False)
    tax = db.Column(db.Numeric, nullable=False)
    city = db.Column(db.Text, nullable=False)
    state = db.Column(db.String(2), nullable=False)
    transaction_num = db.Column(db.String(14), nullable=True, unique=True)
    description = db.Column(db.Text, nullable=True)
    date_time = db.Column(db.DateTime,
                          default=datetime,
                          nullable=False)
    total_id = db.Column(db.Integer, db.ForeignKey(
        'totals.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, purchase_total: float, tax: float,
                 city: str, state: str, transacton_num: str, description: str, date_time: str, total_id: int, user_id: int):
        self.purchase_total = purchase_total
        self.tax = tax
        self.city = city
        self.state = state
        self.transaction_num = transacton_num
        self.description = description
        self.date_time = date_time
        self.total_id = total_id
        self.user_id = user_id

    def serialize(self):
        return {
            'id': self.id,
            'purchase_total': json.dumps(self.purchase_total, use_decimal=True),
            'tax': json.dumps(self.tax, use_decimal=True),
            'city': self.city,
            'state': self.state,
            'transaction_num': self.transaction_num,
            'description': self.description,
            'date_time': self.date_time,
            'total_id': self.total_id,
            'user_id': self.user_id
        }
