from flask import request
from ..models import Receipt, Total, db
from .update_total import update_total


def existing_year(data, user_id, year):
    # data = request.get_json()

    total_id = db.session.query(Total._id).filter(
        Total.tax_year == year).first()[0]
    total = Total.query.get(total_id)

    # [filter through json object to calculate purchase total]
    purchase_total = 0
    for item in data['items']:
        purchase_total += abs(item['amount'])

    # [update existing total (tax year)]
    update_total('sum', total, data['date'][0:4],
                 purchase_total, data['tax'], user_id)
    db.session.commit()

    items = []

    for item in data['items']:
        i = {}
        for key, value in item.items():
            if key == 'amount':
                i['amount'] = abs(value)
            if key == 'description':
                i['description'] = value
            if key == 'qty':
                i['quantity'] = value
        items.append(i)

    new_receipt = Receipt(
        _from=data['merchant_name'],
        purchase_total=float(purchase_total),
        tax=float(data['tax']),
        address=data['merchant_address'],
        items_services=items,
        transaction_number=str(
            data['transaction_number']) if 'transaction_number' in data else None,
        cash=True if data['credit_card_number'] is None or data['payment_method'] == 'cash' else None,
        card_last_4=data['credit_card_number'],
        link=data['merchant_website'],
        date=data['date'],
        time=data['time'],
        total_id=total_id,
        user_id=user_id
    )

    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt
