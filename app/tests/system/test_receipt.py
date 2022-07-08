import os
import json
from datetime import datetime
from api.models import User, Total, Receipt
from ..base_test import BaseTest, _from, purchase_total, tax, address, items_services, transaction_number, cash, card_last_4, link, date, time
from flask_jwt_extended import create_access_token


class TestReceipt(BaseTest):
    def test_create_receipt(self):
        self.maxDiff = None
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                access_token = create_access_token(identity=os.getenv('ADMIN'))
                headers = {
                    "Authorization": "Bearer {}".format(access_token)}

                client.post('/login', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                }, headers=headers)

                response = client.post('/users/home/receipts', json={
                    'from': _from,
                    'purchase_total': purchase_total,
                    'tax': tax,
                    'address': address,
                    'items_services': items_services,
                    'transaction_number': transaction_number,
                    'cash': cash,
                    'card_last_4': card_last_4,
                    'link': link,
                    'date': json.dumps(datetime.strptime(date, "%Y-%m-%d"), indent=4, sort_keys=True, default=str),
                    'time': json.dumps(datetime.strptime(time, "%H:%M:%S"), indent=4, sort_keys=True, default=str)
                }, headers=headers)

                self.assertDictEqual({
                    'from': _from,
                    'purchase_total': purchase_total,
                    'tax': tax,
                    'address': address,
                    'items_services': items_services,
                    'transaction_number': transaction_number,
                    'cash': cash,
                    'card_last_4': card_last_4,
                    'link': link,
                    'date': json.dumps(datetime.strptime(date, "%Y-%m-%d"), indent=4, sort_keys=True, default=str),
                    'time': json.dumps(datetime.strptime(time, "%H:%M:%S"), indent=4, sort_keys=True, default=str)
                }, response.json)

    def test_delete_receipt(self):
        pass

    def test_find_receipt(self):
        pass

    def test_receipt_not_found(self):
        pass

    def test_total_found_with_receipt(self):
        pass

    def test_receipt_list(self):
        pass
