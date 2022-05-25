from re import I
from ..models import Total, User, Receipt, db
from ..commands.update_total import update_total
from ..commands.subtract_from_total import subtract_from_total
from ..commands.validate import validate_datetime
from ..login.home_page import bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request
from sqlalchemy.orm.attributes import flag_modified


# [update user's receipt]


@bp.route('/update_receipt/<receipt_id>', methods=['PATCH', 'PUT'])
@jwt_required(fresh=True)
def update_receipt(receipt_id: int):
    json_data = request.get_json()

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

    if 'tax' in json_data:
        if not isinstance(json_data['tax'], float):
            return jsonify({"error": "Missing a requirement for parsing"})

        # [same as above ^ for tax amount]
        subtract_from_total('tax', receipt, total)
        receipt.tax = json_data['tax']
        db.session.commit()
        update_total('update_tax', total, total.tax_year,
                     total.purchase_totals, receipt.tax, user_id)
    # [update address]
    if 'address' in json_data:
        if not isinstance(json_data['address'], str):
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.city = json_data['address']

    # [update transaction number]
    if 'transaction_number' in json_data:
        if str(json_data['transaction_number']).isnumeric() == False:
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.transaction_num = json_data['transaction_number']

    if 'cash' in json_data:
        if not isinstance(json_data['cash'], bool):
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.cash = json_data['cash']

    if 'card_last_4' in json_data:
        if not isinstance(json_data['card_last_4'], int):
            return jsonify({"error": "Missing a requirement for parsing"})

        receipt.card_last_4 = json_data['card_last_4']

    # [update items_services details]
    if 'items_services' in json_data:
        # [subtract original amount for receipt from annual total]
        subtract_from_total('purchase', receipt, total)
        # [each item or service in JSON]
        for data in json_data['items_services']:
            if 'description' in data:
                # [object key for database checking]
                key = [{'description': data['description']}]
                # [check if query returns object or none]
                if Receipt.query.filter(
                        Receipt.items_services.contains(key)).first():
                    # [each item in object]
                    for item in receipt.items_services:
                        # [to update immutable, JSON object for each iteration]
                        flag_modified(receipt, 'items_services')
                        # [check if item in object matches item in JSON]
                        if item['description'] == data['description']:
                            # [remove old amount from receipt's total]
                            receipt.purchase_total = float(
                                receipt.purchase_total) - float(item['price_per_item']) * float(item['quantity'])

                            if 'quantity' in data and 'price_per_item' in data:
                                # [assign receipt and its total with new amount]
                                receipt.purchase_total = float(
                                    receipt.purchase_total) + float(data['price_per_item']) * float(data['quantity'])

                                item['price_per_item'] = float(
                                    data['price_per_item'])
                                item['quantity'] = int(data['quantity'])

                            elif 'quantity' in data and 'price_per_item' not in data:
                                # [assign receipt and its total with new amount]
                                receipt.purchase_total = float(
                                    receipt.purchase_total) + float(item['price_per_item']) * float(data['quantity'])

                                item['quantity'] = int(data['quantity'])

                            elif 'price_per_item' in data and 'quantity' not in data:
                                # [assign receipt and its total with new amount]
                                receipt.purchase_total = float(
                                    receipt.purchase_total) + float(data['price_per_item']) * float(item['quantity'])

                                item['price_per_item'] = float(
                                    data['price_per_item'])

        # [update annual total with new amount for receipt]
        update_total('update_purchase', total, total.tax_year,
                     receipt.purchase_total, total.tax_totals, user_id)
        db.session.commit()

    # [update date/time]
    if 'date_time' in json_data:
        if validate_datetime('datetime', json_data['date_time']) == False:
            return jsonify({"error": "Date/Time format is incorrect. Please use 'MM-DD-YYYY HH-MM'"})

        # [update total/tax year if provided year is different]
        if int(json_data['date_time'][6: 10]) != total.tax_year:
            try:
                # [get existing total by year]
                total_id = db.session.query(Total._id).filter(
                    Total.tax_year == int(json_data['date_time'][6: 10])).first()[0]
                new_total = Total.query.get_or_404(total_id)

                # [update new total and old total]
                subtract_from_total('', receipt, total)
                update_total('sum', new_total, json_data['date_time'][6: 10],
                             receipt.purchase_total, receipt.tax, user_id)

                receipt.total_id = total_id
                receipt.date_time = json_data['date_time']
                db.session.commit()

            except BaseException:
                # [otherwise create new total by year]
                new_total = Total(
                    purchase_totals=receipt.purchase_total,
                    tax_totals=receipt.tax,
                    tax_year=int(json_data['date_time'][6: 10]),
                    user_id=user_id
                )
                db.session.add(new_total)

                subtract_from_total('', receipt, total)
                # [update receipt info]
                receipt.date_time = json_data['date_time']
                receipt.total_id = new_total._id
                db.session.commit()

        else:
            # [update date_time if year remains the same]
            receipt.date_time = json_data['date_time']
    try:
        db.session.commit()
        return jsonify(receipt.serialize())

    except BaseException as error:
        return jsonify({'error': error})
