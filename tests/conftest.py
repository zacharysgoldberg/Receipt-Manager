from app.api import create_app
from app.api.models.models import User
from dotenv import load_dotenv
import os
import pytest

load_dotenv()


@ pytest.fixture(scope='module')
def new_user():
    user = User('Firstname', 'Lastname', os.getenv('seed_pass'),
                'admin@domain.com', False)
    return user


@ pytest.fixture(scope='module')
def test_client():
    app = create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            yield client
