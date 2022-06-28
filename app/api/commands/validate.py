import re
from datetime import datetime
from ..models import User, db

# [Validate formats]


def validate_date_time(date, time):
    # [Ensure date and time follow format]
    try:
        datetime.strptime(date, "%Y:%m:%d")
        datetime.strptime(time, "%H:%M:%S")
        return date, time
    # [If time is missing seconds, zero them out before return]
    except ValueError:
        correct_time = time + ":00"
        datetime.strptime(correct_time, "%H:%M:%S")
        return date, correct_time


def validate_email(email):
    # [Ensure email follows correct format]
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if regex.fullmatch(email):
        #  [Check if user supplied username exists in db]
        exists = db.session.query(User._id).filter(
            User.email == email).first()
        return exists

    else:
        return False
