from ..login.home_page import bp
from flask import jsonify
from ..commands.subtract_from_total import subtract_from_total
from ..models import Total, User, Receipt, db
from flask_jwt_extended import jwt_required, get_jwt_identity


# [remove receipt]


@ bp.route('/remove_receipt/<receipt_id>', methods=['DELETE'])
@ jwt_required(fresh=True)
def remove_receipt(receipt_id: int):
    user_id = get_jwt_identity()
    # [check if user exists]
    User.query.get_or_404(user_id)

    receipt = Receipt.query.get_or_404(receipt_id)
    tax_year = str(receipt.date_time)[0:4]
    total_id = db.session.query(Total._id).filter(
        Total.tax_year == tax_year).first()[0]
    total = Total.query.get(total_id)

    try:
        # [subtract removed receipt amount from total]
        subtract_from_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify({'removed': receipt.serialize()})

    except BaseException as error:
        return jsonify({'error': error})
