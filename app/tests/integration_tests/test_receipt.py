import os
from api import load
import simplejson as json
from datetime import datetime
from api.models import Receipt, User, Total, db
from ..base_test import(BaseTest, _from, purchase_total, cash,
                        tax, address, items_services, transaction_number,
                        card_last_4, link, date_time)


class ReceiptTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = User.create_user(email=os.getenv('ADMIN'),
                                    password=os.getenv('MAIL_PASSWORD'),
                                    access=2)

            total = Total(purchase_total, tax, date_time[6:10], user._id)

            db.session.add(total)
            db.session.commit()

            receipt = Receipt(
                _from, purchase_total, tax, address, items_services,
                transaction_number, cash, card_last_4, link, datetime.strptime(
                    date_time, '%m-%d-%Y %H:%M'), total._id, user._id
            )
            db.session.add(receipt)
            db.session.commit()
            # [ensure receipt object is not none]
            self.assertIsNotNone(Receipt.query.get(receipt._id))
            # [remove user, total, and receipt objects from db]
            db.session.delete(receipt)
            db.session.delete(total)
            db.session.delete(user)
            db.session.commit()
            # [ensure user, total, and receipt objects are removed from db]
            self.assertIsNone(Receipt.query.get(receipt._id))
            self.assertIsNone(Total.query.get(total._id))
            self.assertIsNone(User.query.get(user._id))

    def test_total_relationship(self):
        user = User.create_user(email=os.getenv('ADMIN'),
                                password=os.getenv('MAIL_PASSWORD'),
                                access=2)

        total = Total(purchase_total, tax, date_time[6:10], user._id)

        db.session.add(total)
        db.session.commit()

        receipt = Receipt(
            _from, purchase_total, tax, address, items_services,
            transaction_number, cash, card_last_4, link, datetime.strptime(
                date_time, '%m-%d-%Y %H:%M'), total._id, 1
        )

        db.session.add(receipt)
        db.session.commit()
        # [ensure receipt FK id equals total id]
        self.assertEqual(receipt.total_id, total._id)

    def test_receipt_json(self):
        self.maxDiff = None
        with self.app_context():
            user = User.create_user(email=os.getenv('ADMIN'),
                                    password=os.getenv('MAIL_PASSWORD'),
                                    access=2)

            total = Total(purchase_total, tax, date_time[6:10], user._id)

            db.session.add(total)
            db.session.commit()

            receipt = Receipt(
                _from, purchase_total, tax, address, items_services,
                transaction_number, cash, card_last_4, link, datetime.strptime(
                    date_time, '%m-%d-%Y %H:%M'), total._id, 1
            )

            db.session.add(receipt)
            db.session.commit()

            expected = {
                'id': receipt._id,
                'from': _from,
                'purchase_total': json.dumps(purchase_total, use_decimal=True),
                'tax': json.dumps(tax, use_decimal=True),
                'address': address,
                'items_services': items_services,
                'transaction_number': transaction_number,
                'cash': cash,
                'card_last_4': card_last_4,
                'link': link,
                'date_time': datetime.strptime(
                    date_time, '%m-%d-%Y %H:%M'),
                'total_id': total._id,
                'user_id': user._id
            }

            self.assertDictEqual(receipt.serialize(), expected)

            db.session.delete(receipt)
            db.session.delete(total)
            db.session.delete(user)
            db.session.commit()

            self.assertIsNone(Receipt.query.get(receipt._id))
            self.assertIsNone(Total.query.get(total._id))
            self.assertIsNone(User.query.get(user._id))
