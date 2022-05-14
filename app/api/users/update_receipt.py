from ..models import Total, User, Receipt, db
from ..commands.update_total import update_total
from ..commands.subtract_from_total import subtract_from_total
from ..commands.validate import validate_datetime
from .users import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import (
    jsonify,
    abort,
    request,
    redirect
)


# [update user's receipt]


@bp.route('/update_receipt/totals/<tax_year>/receipts/<receipt_id>', methods=['PATCH', 'PUT'])
@jwt_required(fresh=True)
def update_receipt(tax_year: int, receipt_id: int):
    data = request.get_json()

    user_id = get_jwt_identity()
    # [get user object]
    user = User.query.get_or_404(user_id)
    # [get total object]
    total_id = db.session.query(Total.id).filter(
        Total.tax_year == tax_year).first()[0]
    total = Total.query.get_or_404(total_id)
    # [get receipt object]
    receipt = Receipt.query.get_or_404(receipt_id)

    lst = ['purchase_total', 'tax', 'city', 'state',
           'transaction_num', 'description', 'date_time']

    # [if none of the items from lst are in json request, return error]
    if all(item not in data for item in lst):
        return abort(400)

    if 'purchase_total' in data:
        if type(data['purchase_total']) != float:
            return abort(400)
        # [subtract original amount for receipt from total]
        subtract_from_total('purchase', receipt, total)
        # a[ssign receipt with new amount]
        receipt.purchase_total = data['purchase_total']
        db.session.commit()
        # [update total with new amount for receipt]
        update_total('update_purchase', total, total.tax_year,
                     receipt.purchase_total, total.tax_totals, user_id)

    if 'tax' in data:
        if type(data['tax']) != float:
            return abort(400)
        # [same as above ^ for tax amount]
        subtract_from_total('tax', receipt, total)
        receipt.tax = data['tax']
        db.session.commit()
        update_total('update_tax', total, total.tax_year,
                     total.purchase_totals, receipt.tax, user_id)
    # [update city]
    if 'city' in data:
        if len(data['city']) < 2:
            return abort(400)

        receipt.city = data['city']
    # [update state]
    if 'state' in data:
        if len(data['state']) != 2:
            return abort(400)

        receipt.state = data['state']
    # [update transaction number]
    if 'transaction_num' in data:
        if str(data['transaction_num']).isnumeric() == False:
            return abort(400)

        receipt.transaction_num = data['transaction_num']
    # [update description]
    if 'description' in data:
        if type(data['description']) != str:
            return abort(400)

        receipt.description = data['description']
    # [update date/time]
    if 'date_time' in data:
        if validate_datetime(data['date_time']) == False:
            return jsonify({"error": "Date-Time format is incorrect. Please use 'MM-DD-YYYY HH-MM'"})

        # [update total/tax year if provided year is different]

        if int(data['date_time'][6:10]) != total.tax_year:
            try:
                # [get existing total by year]
                total_id = db.session.query(Total.id).filter(
                    Total.tax_year == int(data['date_time'][6:10])).first()[0]
                new_total = Total.query.get_or_404(total_id)

                # [update new total and old total]
                subtract_from_total('', receipt, total)
                update_total('sum', new_total, data['date_time'][6:10],
                             receipt.purchase_total, receipt.tax, user_id)

                receipt.total_id = total_id
                receipt.date_time = data['date_time']
                db.session.commit()

            except:
                # [otherwise create new total by year]
                new_total = Total(
                    purchase_totals=receipt.purchase_total,
                    tax_totals=receipt.tax,
                    tax_year=int(data['date_time'][6:10]),
                    user_id=user_id
                )
                db.session.add(new_total)

                subtract_from_total('', receipt, total)
                # [update receipt info]
                receipt.date_time = data['date_time']
                receipt.total_id = new_total.id
                db.session.commit()
        else:
            # [update date_time if year remains the same]
            receipt.date_time = data['date_time']

    try:
        db.session.commit()
        return jsonify(receipt.serialize())

    except:
        return jsonify({'error': 'Unable to fulfill request'})
