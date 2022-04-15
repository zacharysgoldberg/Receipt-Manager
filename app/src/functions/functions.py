import re
from datetime import datetime
from ..models import User, Total, db


def check_datetime(date_time):
    try:
        dt = datetime.strptime(date_time, "%m-%d-%Y %H:%M")
        return True
    except ValueError:
        return False


def subtract_old_total(action, receipt, total):
    if action == 'purchase':
        total.purchase_totals = float(
            total.purchase_totals) - float(receipt.purchase_total)
    elif action == 'tax':
        total.tax_totals = float(total.tax_totals) - float(receipt.tax)
    else:
        total.purchase_totals = float(
            total.purchase_totals) - float(receipt.purchase_total)
        total.tax_totals = float(total.tax_totals) - float(receipt.tax)

    db.session.commit()


def update_total(action, total, year, purchase, tax, user_id):
    # update totals for associated tax year if tax year input exists
    if int(year) == total.tax_year and action == 'sum':
        total.purchase_totals = float(
            total.purchase_totals) + float(purchase)
        total.tax_totals = float(total.tax_totals) + float(tax)

    elif int(year) == total.tax_year and action == 'update_purchase':
        total.purchase_totals = float(
            total.purchase_totals) + float(purchase)

    elif int(year) == total.tax_year and action == 'update_tax':
        total.tax_totals = float(total.tax_totals) + float(tax)

    else:
        total = Total(
            purchase_totals=purchase,
            tax_totals=tax,
            tax_year=year,
            user_id=user_id
        )
        db.session.add(total)


def check_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")

    if regex.fullmatch(email):
        return True

    else:
        return False


def confirm_user(username):
    # for postgres db
    exists = db.session.query(User.id).filter(
        User.username == username).first()
    return exists
