from ..models import Total, User, Receipt, db
from ..commands.update_total import update_total
from ..commands.subtract_from_total import subtract_from_total
from ..commands.validate import validate_datetime
from ..login.home_page import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request


# [update user's receipt]


@bp.route('/update_receipt/<receipt_id>', methods=['PATCH', 'PUT'])
@jwt_required(fresh=True)
def update_receipt(receipt_id: int):
    data = request.get_json()

    user_id = get_jwt_identity()
    # [get user object]
    User.query.get_or_404(user_id)
    # [get receipt object]
    receipt = Receipt.query.get_or_404(receipt_id)
    tax_year = str(receipt.date_time)[0:4]
    # [get total object]
    total_id = db.session.query(Total._id).filter(
        Total.tax_year == int(tax_year)).first()[0]
    total = Total.query.get_or_404(total_id)

    lst = {'purchase_total', 'tax', 'address',
           'transaction_numbers', 'description', 'date_time'}

    # [if none of the items from lst are in json request, return error]
    if all(item not in data for item in lst):
        return jsonify({"error": "Missing a requirement for parsing"})

    if 'purchase_total' in data:
        if not isinstance(data['purchase_total'], float):
            return jsonify({"error": "Missing a requirement for parsing"})

        # [subtract original amount for receipt from total]
        subtract_from_total('purchase', receipt, total)
        # a[ssign receipt with new amount]
        receipt.purchase_total = data['purchase_total']
        db.session.commit()
        # [update total with new amount for receipt]
        update_total('update_purchase', total, total.tax_year,
                     receipt.purchase_total, total.tax_totals, user_id)

    if 'tax' in data:
        if not isinstance(data['tax'], float):
            return jsonify({"error": "Missing a requirement for parsing"})

        # [same as above ^ for tax amount]
        subtract_from_total('tax', receipt, total)
        receipt.tax = data['tax']
        db.session.commit()
        update_total('update_tax', total, total.tax_year,
                     total.purchase_totals, receipt.tax, user_id)
    # [update address]
    if 'address' in data:
        if not isinstance(data['address'], str):
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.city = data['address']

    # [update transaction number]
    if 'transaction_number' in data:
        if str(data['transaction_number']).isnumeric() == False:
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.transaction_num = data['transaction_number']

    if 'cash' in data:
        if not isinstance(data['cash'], bool):
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.cash = data['cash']

    if 'card_last_4' in data:
        if not isinstance(data['card_last_4'], int) or len(data['card_last_4']) != 4:
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.card_last_4 = data['card_last_4']

    # [update description]
    if 'description' in data:
        if isinstance(data['description'], str):
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.description = data['description']

    # [update date/time]
    if 'date_time' in data:
        if validate_datetime('datetime', data['date_time']) == False:
            return jsonify({"error": "Date/Time format is incorrect. Please use 'MM-DD-YYYY HH-MM'"})

        # [update total/tax year if provided year is different]
        if int(data['date_time'][6:10]) != total.tax_year:
            try:
                # [get existing total by year]
                total_id = db.session.query(Total._id).filter(
                    Total.tax_year == int(data['date_time'][6:10])).first()[0]
                new_total = Total.query.get_or_404(total_id)

                # [update new total and old total]
                subtract_from_total('', receipt, total)
                update_total('sum', new_total, data['date_time'][6:10],
                             receipt.purchase_total, receipt.tax, user_id)

                receipt.total_id = total_id
                receipt.date_time = data['date_time']
                db.session.commit()

            except BaseException:
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
                receipt.total_id = new_total._id
                db.session.commit()

        else:
            # [update date_time if year remains the same]
            receipt.date_time = data['date_time']
    try:
        db.session.commit()
        return jsonify(receipt.serialize())

    except BaseException as error:
        return jsonify({'error': error})
