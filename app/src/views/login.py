from flask import Blueprint, jsonify, abort, request, redirect
from ..models.models import Total, User, Receipt, db
from ..commands.commands import check_datetime, update_total, confirm_email, subtract_old_total, check_email
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user


bp = Blueprint('login', __name__, url_prefix='/login')

# Login


@bp.route('', methods=['GET', 'POST'])
def login():
    # Login page
    if request.method == 'GET':
        return 'Login'

    # If neither email, nor password, and remember are used to login, return error
    elif request.method == 'POST' and 'email' not in request.json \
            and 'password' not in request.json and 'remember' not in request.json:
        return abort(400)

    else:
        # check if email exists in db and check if email format is correct
        email = request.json['email'].strip().replace(" ", "")
        print(email)
        if check_email(email) == False or confirm_email(email) is None:
            return "Invalid email"
        # Assign email to variable for filtering primary key
        # check if user exists using email
        user_id = db.session.query(User.id).filter(
            User.email == email).first()[0]
        # get user object
        user = User.query.get(user_id)
        if len(request.json['password']) < 8:
            return 'Password must be at least 8 characters'
        # Assign password to var for checking against db
        password = request.json['password']
        if type(request.json['remember']) != bool:
            return 'Remember me must be set to True or False'
        # Assign remember login cred. to var
        remember = request.json['remember']

        # take user supplied password, hash it, and compare it to hashed password in db. Also check if user object was succesfully created
        if not user or not check_password_hash(user.password, password):
            return 'Please check your credentials and try again.'
        user.authenticated = True
        db.session.add(user)
        db.session.commit()
        # Log user into session
        login_user(user, remember=remember)
        return f'{user.firstname}, logged in Succesfully'


# Get all receipts stored by user


@ bp.route('/successful/<int:id>/receipts_stored', methods=['GET'])
@ login_required
def receipts_stored(id: int):
    user = User.query.get_or_404(id)
    result = [receipt.serialize() for receipt in user.receipts_stored]
    return jsonify(result)


# Get all totals for user


@ bp.route('/successful/<int:id>/totals_stored', methods=['GET'])
@ login_required
def totals_stored(id: int):
    user = User.query.get_or_404(id)
    result = [total.serialize() for total in user.totals_stored]
    return jsonify(result)


# Logout


@ bp.route('/logout')
@ login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect('/login')

# Create new receipt

# Require user to be logged in before adding a receipt


@ bp.route('/successful/<int:id>/add_receipt', methods=['POST'])
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


# Update

# Update user info
@ bp.route('/successful/<int:id>', methods=['PATCH'])
@ login_required
def update_user(id: int):
    user = User.query.get_or_404(id)
    lst = ['password', 'email', 'firstname', 'lastname']

    # If none of items from lst in json request, return error
    if all(item not in request.json for item in lst):
        return abort(400)
    # Update firstname
    if 'firstname' in request.json:
        if request.json['firstname'].strip().isalpha() == False:
            return abort(400)
        user.firstname = request.json['firstname'].title().strip()
    # Update last name
    if 'lastname' in request.json:
        if request.json['lastname'].strip().isalpha() == False:
            return abort(400)
        user.lastname = request.json['lastname'].title().strip()
    # Update password
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        password = request.json['password'].strip().replace(" ", "")
        user.password = generate_password_hash(password)
    # update email
    if 'email' in request.json:
        email = request.json['email'].strip().repalce(" ", "")
        if check_email(email) == False or confirm_email(email) is not None:
            return abort(400)
        user.email = email

    try:
        db.session.commit()
        return jsonify(user.serialize())

    except:
        return jsonify(False)

# Update user's receipt


@bp.route('/successful/<int:user_id>/receipts/<int:receipt_id>', methods=['PATCH', 'PUT'])
@login_required
def update_receipt(user_id: int, receipt_id: int):
    receipt = Receipt.query.get_or_404(receipt_id)
    total_id = db.session.query(Total.id).filter(
        Total.user_id == user_id).first()[0]
    # Get total object
    total = Total.query.get(total_id)
    lst = ['purchase_total', 'tax', 'city', 'state',
           'transaction_num', 'description', 'date_time']

    # If none of the items from lst are in json request, return error
    if all(item not in request.json for item in lst):
        return abort(400)

    if 'purchase_total' in request.json:
        if type(request.json['purchase_total']) != float:
            return abort(400)

        # Subtract original amount for receipt from total
        subtract_old_total('purchase', receipt, total)
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
        subtract_old_total('tax', receipt, total)
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

        # TODO:Update total/tax year id if year is updated
        receipt.date_time = request.json['date_time']

    try:
        db.session.commit()
        return jsonify(receipt.serialize())

    except:
        return jsonify(False)


# Delete

# Remove user
@ bp.route('/successful/<int:id>', methods=['DELETE'])
@ login_required
def delete_user(id: int):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return jsonify(True)
    except:
        return jsonify(False)

# Remove receipt


@ bp.route('/successful/<int:user_id>/remove_receipt/<int:receipt_id>', methods=['DELETE'])
@ login_required
def delete_receipt(user_id: int, receipt_id: int):
    # check user and content exist
    User.query.get_or_404(user_id)
    receipt = Receipt.query.get_or_404(receipt_id)
    tax_year = str(receipt.date_time)[0:4]
    total_id = db.session.query(Total.id).filter(
        Total.tax_year == tax_year).first()[0]
    total = Total.query.get(total_id)

    try:
        # Subtract removed receipt amount from total
        subtract_old_total('', receipt, total)
        db.session.delete(receipt)
        db.session.commit()
        return jsonify(True)

    except:
        return jsonify(False)
