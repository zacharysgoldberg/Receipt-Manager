from unittest import TestCase
from api.models import db
from app import wsgi

"""
BaseTest

The parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

# ['Receipt' seed data]
_from = "Test"
purchase_total = 14.50
tax = 2.50
address = '123 Address, City State Zip'
items_services = {
    "test_item_service": [
        {
            "description": "Description of items /or services",
            "quantity": 2,
            "price_per_item": 5.25
        },
        {
            "description": "Another description of items /or services",
            "quantity": 1,
            "price_per_item": 2.00
        }
    ]
}
transaction_number = "1234567891011"
cash = False
card_last_4 = '1234'
link = 'link'
date_time = "07-10-2022 17:30"

# ['Total' seed data]
purchase_totals = 10.50
tax_totals = 1.50
tax_year = 2022


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        wsgi.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres@localhost:5433/test_db"
        with wsgi.app_context():
            db.init_app(wsgi)

    def setUp(self):
       # [Make sure test database exists]
        with wsgi.app_context():
            db.create_all()
        # Get test client
        self.app = wsgi.test_client
        self.app_context = wsgi.app_context

    def tearDown(self):
        # [Make sure test database is blank]
        with wsgi.app_context():
            db.session.remove()
            db.drop_all()
