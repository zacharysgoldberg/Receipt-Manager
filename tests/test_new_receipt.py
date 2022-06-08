from app.api import create_app
from app.api.models import User, Receipt

# test new receipt


def test_new_receipt(new_receipt):

    assert new_receipt.purchase_total == 20.45
    assert new_receipt.tax == 2.45
    assert new_receipt.city == 'Ventura'
    assert new_receipt.state == 'CA'
    assert new_receipt.transaction_num == '12345678901234'
    assert new_receipt.description == 'Pants'
    assert new_receipt.date_time == '04-01-2022 14:00:00'
    assert new_receipt.total_id == 1
    assert new_receipt.user_id == 1
