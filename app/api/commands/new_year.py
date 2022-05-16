from ..models import Total, Receipt, db
from flask import abort, request, redirect


def new_year(user_id):
    data = request.get_json()
    # [get row count]
    rows = db.session.query(Total).count()

    total = Total(
        purchase_totals=data['purchase_total'],
        tax_totals=data['tax'],
        tax_year=int(data['date_time'][6:10]),
        user_id=user_id
    )
    db.session.add(total)

    purchase_total = data['purchase_total']
    tax = data['tax'],
    city = data['city'],
    state = data['state'],
    transaction_number = str(data['transaction_number']) if 'transaction_number' in data and str(data['transaction_number']).isnumeric(
    ) == True else None,
    description = data['description'] if 'description' in data else None,
    date_time = data['date_time'],
    total_id = rows + 1,
    user_id = user_id

    # [add new receipt for new tax year]
    new_receipt = Receipt.add_receipt(
        purchase_total, tax, city, state,
        transaction_number, description, date_time, total_id,
        user_id
    )

    return new_receipt
