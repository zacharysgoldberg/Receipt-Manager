import re
from datetime import datetime
from ..models import User, db

# Ensure date and time follow correct format


def validate_datetime(date_time):
    try:
        datetime.strptime(date_time, "%m-%d-%Y %H:%M")
        return True
    except ValueError:
        return False


def validate_email(email):
    # Ensure email follows correct format
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if regex.fullmatch(email):
        #  Check if user supplied username exists in db
        exists = db.session.query(User.id).filter(
            User.email == email).first()
        return exists
    else:
        return False
