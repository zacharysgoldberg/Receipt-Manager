from app.api import create_app
from app.api.models.models import User
import pytest


@pytest.fixture(scope='module')
def new_user():
    user = User('Firstname', 'Lastname', 'admin123',
                'admin@domain.com', False)
    return user


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        # Establish an application context
        with app.app_context():
            yield client
