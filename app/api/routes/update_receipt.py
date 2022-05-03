from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import check_datetime, update_total, confirm_email, subtract_from_total
from flask_login import login_required
from ..commands import existing_year, new_year
from .login import bp


# Update user's receipt


@bp.route('/logged_in/<user_id>/totals/<total_id>/receipts/<receipt_id>', methods=['PATCH', 'PUT'])
@login_required
def update_receipt(user_id: int, total_id: int, receipt_id: int):
    # Get user object
    user = User.query.get_or_404(user_id)
    # Get total object
    total = Total.query.get_or_404(total_id)
    # Get receipt object
    receipt = Receipt.query.get_or_404(receipt_id)

    lst = ['purchase_total', 'tax', 'city', 'state',
           'transaction_num', 'description', 'date_time']

    # If none of the items from lst are in json request, return error
    if all(item not in request.json for item in lst):
        return abort(400)

    if 'purchase_total' in request.json:
        if type(request.json['purchase_total']) != float:
            return abort(400)
        # Subtract original amount for receipt from total
        subtract_from_total('purchase', receipt, total)
        # Assign receipt with new amount
        receipt.purchase_total = request.json['purchase_total']
        db.session.commit()
        # Update total with new amount for receipt
        update_total('update_purchase', total, total.tax_year,
                     receipt.purchase_total, total.tax_totals, user_id)

    if 'tax' in request.json:
        if type(request.json['tax']) != float:
            return abort(400)
        # Same as above ^ for tax amount
        subtract_from_total('tax', receipt, total)
        receipt.tax = request.json['tax']
        db.session.commit()
        update_total('update_tax', total, total.tax_year,
                     total.purchase_totals, receipt.tax, user_id)
    # Ud=pdate city
    if 'city' in request.json:
        if len(request.json['city']) < 2:
            return abort(400)

        receipt.city = request.json['city']
    # Update state
    if 'state' in request.json:
        if len(request.json['state']) != 2:
            return abort(400)

        receipt.state = request.json['state']
    # Update transaction number
    if 'transaction_num' in request.json:
        if str(request.json['transaction_num']).isnumeric() == False:
            return abort(400)

        receipt.transaction_num = request.json['transaction_num']
    # Update description
    if 'description' in request.json:
        if type(request.json['description']) != str:
            return abort(400)

        receipt.description = request.json['description']
    # Update date/time
    if 'date_time' in request.json:
        if check_datetime(request.json['date_time']) == False:
            return abort(400)

        # Update total/tax year if provided year is different

        if int(request.json['date_time'][6:10]) != total.tax_year:
            try:
                # get existing total by year
                total_id = db.session.query(Total.id).filter(
                    Total.tax_year == int(request.json['date_time'][6:10])).first()[0]
                new_total = Total.query.get_or_404(total_id)

                # update new total and old total
                subtract_from_total('', receipt, total)
                update_total('sum', new_total, request.json['date_time'][6:10],
                             receipt.purchase_total, receipt.tax, user_id)

                receipt.total_id = total_id
                receipt.date_time = request.json['date_time']
                db.session.commit()

            except:
                # otherwise create new total by year
                new_total = Total(
                    purchase_totals=receipt.purchase_total,
                    tax_totals=receipt.tax,
                    tax_year=int(request.json['date_time'][6:10]),
                    user_id=user_id
                )
                db.session.add(new_total)

                subtract_from_total('', receipt, total)
                # update receipt info
                receipt.date_time = request.json['date_time']
                receipt.total_id = new_total.id
                db.session.commit()
        else:
            # update date_time if year remains the same
            receipt.date_time = request.json['date_time']

    try:
        db.session.commit()
        return jsonify(receipt.serialize())

    except:
        return jsonify(False)
