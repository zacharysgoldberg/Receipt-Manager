import re
from datetime import datetime
from ..models import User, db

# Ensure date and time follow correct format


def validate_time(time):
    if datetime.strptime(time, "%H:%M") is True:
        new_time = datetime.time.strptime(time, "%H:%M:%S")
        return new_time

    return time


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
