from app import app
from unittest import TestCase

# [error message for unit tests]


def error_message(value):
    return f"The '{value}' of the receipt after creation does not equal the constructor argument."


class UnitBaseTest(TestCase):
    pass
