from ..models.models import User, Total, db


# Subtract previous receipt amount from respective tax year total


def subtract_from_total(action, receipt, total):
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


# update totals for respective tax year if user supplied tax year input exists
def update_total(action, total, year, purchase, tax, user_id):
    if total.tax_year == int(year) and action == 'sum':
        total.purchase_totals = float(
            total.purchase_totals) + float(purchase)
        total.tax_totals = float(total.tax_totals) + float(tax)

    elif total.tax_year == int(year) and action == 'update_purchase':
        total.purchase_totals = float(
            total.purchase_totals) + float(purchase)

    elif total.tax_year == int(year) and action == 'update_tax':
        total.tax_totals = float(total.tax_totals) + float(tax)

    else:
        # Create new tax year total
        total = Total(
            purchase_totals=purchase,
            tax_totals=tax,
            tax_year=int(year),
            user_id=user_id
        )
        db.session.add(total)
