import simplejson as json
from api.models import Receipt
from .unit_base_test import UnitBaseTest, error_message

receipt = Receipt(
    '_from', 5.00, 0.50, 'address', {},
    '1234567891011', False, '1234', 'link', '07-10-2022', 1, 1


)

# [testing receipt model]


class ReceiptTest(UnitBaseTest):
    def test_create_receipt(self):
        self.assertEqual('_from', receipt._from, error_message('from'))
        self.assertEqual(5.00, receipt.purchase_total,
                         error_message('purchase_total'))
        self.assertEqual(0.50, receipt.tax, error_message('tax'))
        self.assertEqual('address', receipt.address, error_message('address'))
        self.assertDictEqual({}, receipt.items_services,
                             error_message('items_services'))
        self.assertEqual('1234567891011',
                         receipt.transaction_number, error_message('transaction_number'))
        self.assertEqual(False, receipt.cash, error_message('cash'))
        self.assertEqual('1234', receipt.card_last_4,
                         error_message('card_last_4'))
        self.assertEqual('link', receipt.link, error_message('link'))
        self.assertEqual('07-10-2022', receipt.date_time,
                         error_message('date_time'))
        self.assertEqual(1, receipt.total_id, error_message('total_id'))
        self.assertEqual(1, receipt.user_id, error_message('user_id'))

    def test_serializer_no_receipts(self):
        self.maxDiff = None
        expected = {
            'id': None,
            'from': '_from',
            'purchase_total': json.dumps(5.00, use_decimal=True),
            'tax': json.dumps(0.50, use_decimal=True),
            'address': 'address',
            'items_services': {},
            'transaction_number': '1234567891011',
            'cash': False,
            'card_last_4': '1234',
            'link': 'link',
            'date_time': '07-10-2022',
            'total_id': 1,
            'user_id': 1
        }

        self.assertEqual(expected, receipt.serialize(),
                         f"The JSON export of the receipt is incorrect. Received {receipt.serialize()}, expected {expected}")
