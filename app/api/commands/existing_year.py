from flask import abort, request, redirect
from .update_total import update_total
from ..models import Total, Receipt, db


def existing_year(user_id, year):
    total_id = db.session.query(Total._id).filter(
        Total.tax_year == year).first()[0]
    total = Total.query.get(total_id)
    # Update existing total (tax year)
    update_total('sum', total, request.json['date_time'][6:10],
                 request.json['purchase_total'], request.json['tax'], id)
    db.session.commit()

    # Add new receipt for existing tax year
    receipt = Receipt(
        purchase_total=request.json['purchase_total'],
        tax=request.json['tax'],
        city=request.json['city'],
        state=request.json['state'],
        transacton_num=str(request.json['transaction_num']) if 'transaction_num' in request.json and str(request.json['transaction_num']).isnumeric(
        ) == True else None,
        description=request.json['description'] if 'description' in request.json else None,
        date_time=request.json['date_time'],
        total_id=total_id,
        user_id=user_id
    )

    db.session.add(receipt)
    db.session.commit()
    return receipt
