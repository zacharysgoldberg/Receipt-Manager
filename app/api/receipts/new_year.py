from ..models import Total, Receipt, db
from flask import request


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

    # [add new receipt for new tax year]
    new_receipt = Receipt(
        _from=data['from'],
        purchase_total=data['purchase_total'],
        tax=data['tax'],
        address=data['address'],
        transaction_number=str(data['transaction_number']) if 'transaction_number' in data and str(data['transaction_number']).isnumeric(
        ) == True else None,
        category=data['category'],
        description=data['description'] if 'description' in data else None,
        cash=data['cash'] if 'cash' in data else None,
        card_last_4=data['card_last_4'] if 'card_last_4' in data else None,
        date_time=data['date_time'],
        total_id=rows + 1,
        user_id=user_id
    )

    db.session.add(new_receipt)
    db.session.commit()

    return new_receipt
