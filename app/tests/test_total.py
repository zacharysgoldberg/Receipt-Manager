import json
from .base_test import BaseTest
from api.models import Total


purchase_totals = 10.50
tax_totals = 1.50
tax_year = 2022

total = Total(purchase_totals, tax_totals, tax_year, 1)


class TotalTest(BaseTest):
    def test_create_total(self):
        self.assertEqual(purchase_totals, total.purchase_totals)
        self.assertEqual(tax_totals, total.tax_totals)
        self.assertEqual(tax_year, total.tax_year)
        self.assertEqual(1, total.user_id)

    def test_total_serializer(self):
        expected = {
            'id': None,
            'purchase_totals': json.dumps(purchase_totals),
            'tax_totals': json.dumps(tax_totals),
            'tax_year': tax_year,
            'user_id': 1
        }

        self.assertDictEqual(expected, total.serialize())
