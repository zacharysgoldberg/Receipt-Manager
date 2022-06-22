import os
from api import load
from datetime import datetime
import simplejson as json
from api.models import Total, User, Receipt, db
from ..base_test import (BaseTest, _from, purchase_total, tax,
                         address, items_services, transaction_number,
                         cash, card_last_4, link, date_time,
                         purchase_totals, tax_totals, tax_year)


class TotalTest(BaseTest):
    def test_create_total(self):
        total = Total(purchase_totals, tax_totals, tax_year, 1)

        self.assertListEqual(total.receipt_totals.all(), [])

    def test_crud(self):
        with self.app_context():
            user = User.create_user(email=os.getenv('ADMIN'),
                                    password=os.getenv('MAIL_PASSWORD'),
                                    access=2)
            total = Total(purchase_totals, tax_totals, tax_year, user._id)

            self.assertIsNone(Total.query.get(total._id))

            db.session.add(total)
            db.session.commit()

            self.assertIsNotNone(Total.query.get(total._id))

            db.session.delete(total)
            db.session.delete(user)
            db.session.commit()

            self.assertIsNone(Total.query.get(total._id))
            self.assertIsNone(User.query.get(user._id))

    def test_total_relationship(self):
        with self.app_context():
            user = User.create_user(email=os.getenv('ADMIN'),
                                    password=os.getenv('MAIL_PASSWORD'),
                                    access=2)

            total = Total(purchase_totals, tax_totals, tax_year, user._id)

            db.session.add(total)
            db.session.commit()

            receipt = Receipt(
                _from, purchase_total, tax, address, items_services,
                transaction_number, cash, card_last_4, link, datetime.strptime(
                    date_time, '%m-%d-%Y %H:%M'), total._id, user._id
            )
            db.session.add(receipt)
            db.session.commit()

            self.assertEqual(total.receipt_totals.count(), 1)
            self.assertEqual(
                total.receipt_totals.first().total_id, total._id)

            db.session.delete(receipt)
            db.session.delete(total)
            db.session.delete(user)
            db.session.commit()

            self.assertIsNone(Total.query.get(total._id))
            self.assertIsNone(User.query.get(user._id))

    def test_total_json(self):
        with self.app_context():
            user = User.create_user(email=os.getenv('ADMIN'),
                                    password=os.getenv('MAIL_PASSWORD'),
                                    access=2)

            total = Total(purchase_totals, tax_totals, tax_year, user._id)

            db.session.add(total)
            db.session.commit()

            expected = {
                'id': total._id,
                'purchase_totals': json.dumps(purchase_totals, use_decimal=True),
                'tax_totals': json.dumps(tax_totals, use_decimal=True),
                'tax_year': tax_year,
                'user_id': user._id
            }

            self.assertDictEqual(total.serialize(), expected)

            db.session.delete(total)
            db.session.delete(user)
            db.session.commit()

            self.assertIsNone(Total.query.get(total._id))
            self.assertIsNone(User.query.get(user._id))
