from unittest import TestCase
from ..test_receipt import (
    _from, purchase_total, transaction_number, tax, receipt,
    address, cash, card_last_4, link, date_time
)


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


class ReceiptTest(TestCase):
    def test_create_receipt(self):
        self.assertEqual(_from, receipt._from)
        self.assertEqual(purchase_total, receipt.purchase_total)
        self.assertEqual(tax, receipt.tax)
        self.assertEqual(address, receipt.address)
        self.assertEqual(items_services, receipt.items_services)
        self.assertDictEqual(items_services, receipt.items_services)
        self.assertEqual(transaction_number, receipt.transaction_number)
        self.assertEqual(cash, receipt.cash)
        self.assertEqual(card_last_4, receipt.card_last_4)
        self.assertEqual(link, receipt.link)
        self.assertEqual(date_time, receipt.date_time)
