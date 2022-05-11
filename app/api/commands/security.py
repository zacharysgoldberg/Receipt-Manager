from ..models.models import User, db
from werkzeug.security import check_password_hash
import re


# Ensure email follows correct format


def check_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if regex.fullmatch(email):
        return True

    else:
        return False

# Check if user supplied username exists in db


def validate_email(email):
    exists = db.session.query(User.id).filter(
        User.email == email).first()
    return exists
