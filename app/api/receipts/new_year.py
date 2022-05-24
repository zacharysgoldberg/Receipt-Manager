from ..models import Total, Receipt, db
from flask import request


def new_year(user_id):
    data = request.get_json()
    # [get row count]
    rows = db.session.query(Total).count()

    # [filter through json object to calculate purchase total]
    purchase_total = 0
    for item in data['items_services']:
        purchase_total += item['price_per_item'] * item['quantity']

    total = Total(
        purchase_totals=float(purchase_total),
        tax_totals=float(data['tax']),
        tax_year=int(data['date_time'][6:10]),
        user_id=user_id
    )
    db.session.add(total)

    # [add new receipt for new tax year]
    new_receipt = Receipt(
        _from=data['from'],
        purchase_total=float(purchase_total),
        tax=float(data['tax']),
        address=data['address'],
        items_services=data['items_services'],
        transaction_number=str(data['transaction_number']) if 'transaction_number' in data and str(data['transaction_number']).isnumeric(
        ) == True else None,
        cash=data['cash'] if 'cash' in data else None,
        card_last_4=data['card_last_4'] if 'card_last_4' in data else None,
        date_time=data['date_time'],
        total_id=rows + 1,
        user_id=user_id
    )

    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt
