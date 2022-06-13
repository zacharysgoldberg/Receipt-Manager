from decimal import Decimal
from .base_test import BaseTest
import json
from api.models import Receipt

_from = "Test"
purchase_total = 14.50
tax = 2.50
address = '123 Address, City State Zip'
transaction_number = "1234567891011"
cash = None
card_last_4 = '1234'
link = None
date_time = "07-10-2022 17:30"


receipt = Receipt(
    _from, purchase_total, tax, address, {},
    transaction_number, cash, card_last_4, link, date_time, 1, 1
)

# [testing receipt model]


class ReceiptTest(BaseTest):
    def test_create_receipt(self):
        self.assertEqual(_from, receipt._from)
        self.assertEqual(purchase_total, receipt.purchase_total)
        self.assertEqual(tax, receipt.tax)
        self.assertEqual(address, receipt.address)
        self.assertDictEqual({}, receipt.items_services)
        self.assertEqual(transaction_number, receipt.transaction_number)
        self.assertEqual(cash, receipt.cash)
        self.assertEqual(card_last_4, receipt.card_last_4)
        self.assertEqual(link, receipt.link)
        self.assertEqual(date_time, receipt.date_time)

    def test_serializer_no_receipts(self):
        self.maxDiff = None
        expected = {
            'id': None,
            'from': _from,
            'purchase_total': json.dumps(purchase_total),
            'tax': json.dumps(tax),
            'address': address,
            'items_services': {},
            'transaction_number': transaction_number,
            'cash': cash,
            'card_last_4': card_last_4,
            'link': link,
            'date_time': date_time,
            'total_id': 1,
            'user_id': 1
        }

        self.assertDictEqual(expected, receipt.serialize())
