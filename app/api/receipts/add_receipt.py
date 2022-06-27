import json
from flask import jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from ..commands import new_year
from ..commands import existing_year
from ..models import User
from .receipt_ocr import receipt_ocr
from ..users.users_admin import bp


# [create new receipt]


@ bp.route('/home/receipts', methods=['GET', 'POST'])
<<<<<<< HEAD
# @jwt_required()
=======
@jwt_required()
>>>>>>> 72bdfc1 (updated root directory)
def add_receipt():
    """ data = request.get_json()
        try:
            user_id = get_jwt_identity()
            User.query.get_or_404(user_id)

            # [add new receipt to existing tax year total]
            # receipt = existing_year.existing_year(
            #     user_id, int(data['date_time'][6:10]))
            return jsonify(receipt.serialize())

        except BaseException:
            # [add new receipt to new tax year total]
            receipt = new_year.new_year(user_id)
            return jsonify(receipt.serialize())"""
    if request.method == 'GET':
<<<<<<< HEAD
        # user_id = get_jwt_identity()
        # user = User.query.get_or_404(user_id)
        # receipts = [receipt.serialize() for receipt in user.receipts_stored]
        # , jsonfile=json.dumps(receipts))
        return render_template('receipts.html')

    elif request.method == 'POST':
        # verify_jwt_in_request()
=======
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        receipts = [receipt.serialize()
                    for receipt in user.receipts_stored]
        jsonfile = json.dumps(receipts)
        return render_template('receipts.html', jsonfile=jsonfile)

    elif request.method == 'POST':
        verify_jwt_in_request()
>>>>>>> 72bdfc1 (updated root directory)
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save(uploaded_file.filename)

<<<<<<< HEAD
        receipt_ocr(request.files['file'])
=======
        receipt = receipt_ocr(uploaded_file)

        try:
            user_id = get_jwt_identity()
            User.query.get_or_404(user_id)

            # [add new receipt to existing tax year total]
            existing_year.existing_year(
                receipt[0], user_id, int(receipt[0]['date'][0:4]))

        except BaseException:
            # [add new receipt to new tax year total]
            new_year.new_year(receipt[0], user_id)
>>>>>>> 72bdfc1 (updated root directory)

        return redirect(url_for('users.add_receipt'))
