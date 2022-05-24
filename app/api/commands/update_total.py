from ..models import Total, db


# [update totals for respective tax year if user supplied tax year input exists]
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
        # [create new tax year total]
        total = Total(
            purchase_totals=float(purchase),
            tax_totals=float(tax),
            tax_year=int(year),
            user_id=user_id
        )
        db.session.add(total)
