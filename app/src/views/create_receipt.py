from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import check_datetime, update_total
from flask_login import login_required
from .login import bp

# Create new receipt

# Require user to be logged in before adding a receipt


@ bp.route('/logged_in/<int:id>/add_receipt', methods=['POST'])
@ login_required
def add_receipt(id: int):
    User.query.get_or_404(id)

    lst = ['purchase_total', 'tax', 'city', 'state', 'date_time']
    if any(item not in request.json for item in lst) \
            or type(request.json['purchase_total']) != float\
            or type(request.json['tax']) != float \
            or request.json['city'].isalpha() == False \
            or request.json['state'].isalpha() == False \
            or check_datetime(request.json['date_time']) == False:
        return abort(400)

    try:
        total_id = db.session.query(Total.id).filter(
            Total.user_id == id).first()[0]
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
            user_id=id
        )

        db.session.add(receipt)
        db.session.commit()
        return jsonify(receipt.serialize())

    except:
        rows = db.session.query(Total).count()

        total = Total(
            purchase_totals=request.json['purchase_total'],
            tax_totals=request.json['tax'],
            tax_year=request.json['date_time'][6:10],
            user_id=id
        )
        db.session.add(total)

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
            total_id=rows + 1,
            user_id=id
        )

        db.session.add(receipt)
        db.session.commit()
        return jsonify(receipt.serialize())
