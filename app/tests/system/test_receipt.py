import os
import json
from api.models import User, Total, Receipt
from ..base_test import BaseTest, _from, purchase_total, tax, address, items_services, transaction_number, cash, card_last_4, link, date_time


class TestReceipt(BaseTest):
    def test_create_receipt(self):
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                client.post('/login', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                }, headers={'Content-Type': 'application/json'})

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
                    'date_time': date_time

                })

                """self.assertDictEqual({
                    'from': _from,
                    'purchase_total': purchase_total,
                    'tax': tax,
                    'address': address,
                    'items_services': items_services,
                    'transaction_number': transaction_number,
                    'cash': cash,
                    'card_last_4': card_last_4,
                    'link': link,
                    'date_time': date_time
                }, json.loads(response.json))"""

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
