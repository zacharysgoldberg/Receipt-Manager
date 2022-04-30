from app.api import create_app
from app.api.models.models import User, db

# test login page


def test_login_page():
    app = create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        response = client.get('/login')
        assert response.status_code == 200
        assert b"Login" in response.data


# test login credentials


def test_login():
    app = create_app()
    with app.test_client() as client:
        response = client.post(
            '/login', json={'email': 'admin@domain.com', 'password': 'admin123', 'remember': True}, content_type='application/json')
        assert response.status_code == 200
        assert b", logged in Succesfully" in response.data


# test logout


def test_logout():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/login/logged_out')
        assert response.status_code == 302
        assert b"/login" in response.data
