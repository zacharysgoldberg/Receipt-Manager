from ..models import Total, Receipt, db
from flask import request


<<<<<<< HEAD
def new_year(user_id):
    data = request.get_json()
=======
def new_year(data, user_id):
    # data = request.get_json()
>>>>>>> 72bdfc1 (updated root directory)
    # [get row count]
    rows = db.session.query(Total).count()

    # [filter through json object to calculate purchase total]
    purchase_total = 0
<<<<<<< HEAD
    for item in data['items_services']:
        purchase_total += item['price_per_item'] * item['quantity']
=======
    for item in data['items']:
        purchase_total += item['amount']
>>>>>>> 72bdfc1 (updated root directory)

    total = Total(
        purchase_totals=float(purchase_total),
        tax_totals=float(data['tax']),
<<<<<<< HEAD
        tax_year=int(data['date_time'][6:10]),
=======
        tax_year=int(data['date'][0:4]),
>>>>>>> 72bdfc1 (updated root directory)
        user_id=user_id
    )
    db.session.add(total)

    # [add new receipt for new tax year]
    new_receipt = Receipt(
<<<<<<< HEAD
        _from=data['from'],
        purchase_total=float(purchase_total),
        tax=float(data['tax']),
        address=data['address'],
        items_services=data['items_services'],
        transaction_number=str(data['transaction_number']) if 'transaction_number' in data and str(data['transaction_number']).isnumeric(
        ) == True else None,
        cash=data['cash'] if 'cash' in data else None,
        card_last_4=data['card_last_4'] if 'card_last_4' in data else None,
        link=data['link'] if 'link' in data else None,
        date_time=data['date_time'],
=======
        _from=data['merchant_name'],
        purchase_total=float(purchase_total),
        tax=float(data['tax']),
        address=data['merchant_address'],
        items_services=data['items'],
        transaction_number=str(
            data['transaction_number']) if 'transaction_number' in data else None,
        cash=True if data['credit_card_number'] is None or data['payment_method'] == 'cash' else None,
        card_last_4=data['credit_card_number'],
        link=data['merchant_website'],
        date=data['date'],
        time=data['time'],
>>>>>>> 72bdfc1 (updated root directory)
        total_id=rows + 1,
        user_id=user_id
    )

    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt
