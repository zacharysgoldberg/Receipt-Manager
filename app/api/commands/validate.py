import re
from datetime import datetime
from ..models import User, db

# Ensure date and time follow correct format

# TODO:Fix Time formatting


def validate_date_time(_type, date_or_time):
    if _type == 'date':
        try:
            datetime.strptime(date_or_time, "%y:%m:%d")
        except ValueError:
            raise ValueError("Incorrect date format. YYYY-MMM-DD")

    if _type == 'time':
        try:
            datetime.strptime(date_or_time, "%H:%M")
        except ValueError:
            raise ValueError("Incorrect time format. HH:MM")

    return date_or_time


def validate_email(email):
    # Ensure email follows correct format
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if regex.fullmatch(email):
        #  Check if user supplied username exists in db
        exists = db.session.query(User._id).filter(
            User.email == email).first()
        return exists

    else:
        return False
