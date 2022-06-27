from ..models import Total, Receipt, db
from ..commands.validate import validate_time


def new_year(data, user_id):
    # data = request.get_json()
    # [get row count]
    rows = db.session.query(Total).count()

    # [filter through json object to calculate purchase total]
    purchase_total = 0
    for item in data['items']:
        purchase_total += item['amount']

    total = Total(
        purchase_totals=float(purchase_total),
        tax_totals=float(data['tax']),
        tax_year=int(data['date'][0:4]),
        user_id=user_id
    )
    db.session.add(total)

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

    # [add new receipt for new tax year]
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
        total_id=rows + 1,
        user_id=user_id
    )

    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt
