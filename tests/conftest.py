from app.api import create_app
from app.api.models import User, Receipt
from dotenv import load_dotenv
import os
import pytest

load_dotenv()


@pytest.fixture(scope='module')
def new_user():
    email = 'admin@domain.com'
    user = User('Firstname', 'Lastname', email, os.getenv(
        'SEED_PASS'), email.split('@')[0])
    return user


@pytest.fixture(scope='module')
def new_receipt():
    receipt = Receipt(20.45, 2.45, 'Ventura',
                      'CA', '12345678901234', 'Pants', '04-01-2022 14:00:00', 1, 1)
    return receipt


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            yield client
