from flask import request
from ..models import Receipt, Total, db
from .update_total import update_total


<<<<<<< HEAD
def existing_year(user_id, year):
    data = request.get_json()
=======
def existing_year(data, user_id, year):
    # data = request.get_json()
>>>>>>> 72bdfc1 (updated root directory)

    total_id = db.session.query(Total._id).filter(
        Total.tax_year == year).first()[0]
    total = Total.query.get(total_id)

    # [filter through json object to calculate purchase total]
    purchase_total = 0
<<<<<<< HEAD
    for item in data['items_services']:
        purchase_total += item['price_per_item'] * item['quantity']

    # [update existing total (tax year)]
    update_total('sum', total, data['date_time'][6:10],
=======
    for item in data['items']:
        purchase_total += abs(item['amount'])

    # [update existing total (tax year)]
    update_total('sum', total, data['date'][0:4],
>>>>>>> 72bdfc1 (updated root directory)
                 purchase_total, data['tax'], user_id)
    db.session.commit()

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
        total_id=total_id,
        user_id=user_id
    )

    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt
