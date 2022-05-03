from ..models.models import Total, User, Receipt, db
from flask import Blueprint, jsonify, abort, request, redirect
from ..commands.commands import check_datetime, update_total
import asyncio


def new_year(id):
    # Get row count
    rows = db.session.query(Total).count()

    total = Total(
        purchase_totals=request.json['purchase_total'],
        tax_totals=request.json['tax'],
        tax_year=int(request.json['date_time'][6:10]),
        user_id=id
    )
    db.session.add(total)

    # Add new receipt for new tax year
    receipt = Receipt(
        purchase_total=request.json['purchase_total'],
        tax=request.json['tax'],
        city=request.json['city'],
        state=request.json['state'],
        transacton_num=str(request.json['transaction_num']) if 'transaction_num' in request.json and str(request.json['transaction_num']).isnumeric(
        ) == True else None,
        description=request.json['description'] if 'description' in request.json else None,
        date_time=request.json['date_time'],
        total_id=rows + 1,
        user_id=id
    )

    db.session.add(receipt)
    db.session.commit()
    return receipt
