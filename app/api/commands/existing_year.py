from flask import abort, request, redirect
from .update_total import update_total
from ..models import Total, Receipt, db


def existing_year(user_id, year):
    data = request.get_json()

    total_id = db.session.query(Total._id).filter(
        Total.tax_year == year).first()[0]
    total = Total.query.get(total_id)
    # [update existing total (tax year)]
    update_total('sum', total, data['date_time'][6:10],
                 data['purchase_total'], data['tax'], id)
    db.session.commit()

    new_receipt = Receipt.add_receipt(
        _from=data['from'],
        purchase_total=data['purchase_total'],
        tax=data['tax'],
        address=data['address'],
        transacton_number=str(data['transaction_number']) if 'transaction_number' in data and str(data['transaction_number']).isnumeric(
        ) == True else None,
        description=data['description'] if 'description' in data else None,
        cash=data['cash'] if 'cash' in data else None,
        card_last_4=data['card_last_4'] if 'card_last_4' in data else None,
        date_time=data['date_time'],
        total_id=total_id,
        user_id=user_id
    )

    return new_receipt
