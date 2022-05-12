from app.api import create_app
from dotenv import load_dotenv
from app.api.models.models import User, db
from flask_jwt_extended import create_access_token, get_jwt
import os

load_dotenv()

# [test login page]


def test_login_page():
    app = create_app()
    # [create a test client using the Flask application configured for testing]
    with app.test_client() as client:
        response = client.get('/login')
        assert response.status_code == 200
        assert b"Login" in response.data


# [test login credentials]


def test_login():
    app = create_app()
    with app.test_client() as client:
        response = client.post(
            '/login', json={'email': 'admin@domain.com', 'password': os.getenv('SEED_PASS')}, content_type=f'application/json')
        assert response.status_code == 200
        assert b"access_token" in response.data


# [test logout]
"""
def test_logout():
    app = create_app()
    app.app_context()
    with app.test_client() as client:
        access_token = create_access_token(identity=1, fresh=True)
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        response = client.post('/login/logged_out', authorization=headers)
        assert response.status_code == 200
        assert b"/login" in response.data"""
