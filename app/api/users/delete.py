from ..models import Total, User, Receipt, db
from ..commands.subtract_from_total import subtract_from_total
from flask_jwt_extended import jwt_required, get_jwt_identity
from .users import bp
from flask import(
    jsonify,
    abort,
    request,
    redirect
)


# [remove user]


@ bp.route('/delete_account', methods=['DELETE'])
@jwt_required(fresh=True)
def delete_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'deleted_account': user.serialize()})

    except:
        return jsonify({'error': 'Unable to fulfill request'})

# [remove receipt]


@ bp.route('/remove_receipt/<receipt_id>', methods=['DELETE'])
@ jwt_required(fresh=True)
def remove_receipt(receipt_id: int):
    user_id = get_jwt_identity()
    # [check if user exists]
    User.query.get_or_404(user_id)

    receipt = Receipt.query.get_or_404(receipt_id)
    tax_year = str(receipt.date_time)[0:4]
    total_id = db.session.query(Total.id).filter(
        Total.tax_year == tax_year).first()[0]
    total = Total.query.get(total_id)

    try:
        # [subtract removed receipt amount from total]
        subtract_from_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify({'removed': receipt.serialize()})

    except:
        return jsonify({'error': 'Unable to fulfill request'})
