from ..users.users_admin import bp
from flask import jsonify, render_template
from ..models import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json


# [get all totals for user]


@ bp.route('/home/totals')
@ jwt_required()
def totals_stored():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    totals = [total.serialize() for total in user.totals_stored]
    # json_resp = jsonify(result)
    return render_template('totals.html', jsonfile=json.dumps(totals))
