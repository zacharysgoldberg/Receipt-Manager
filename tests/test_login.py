from app.src import create_app
import json
import pytest

# testing login page


def test_login_page():
    app = create_app()
    # Create a test client using the Flask application configured for testing
    with app.test_client() as client:
        response = client.get('/login')
        assert response.status_code == 200
        assert b"Login" in response.data

# testing login credentials


def test_login():
    app = create_app()
    with app.test_client() as client:
        response = client.post(
            '/login', json={'email': 'admin@gmail.com', 'password': 'admin123', 'remember': 'yes'}, content_type='application/json')
        assert response.status_code == 200
        assert b"logged in Succesfully" in response.data


# testing logout


def test_logout():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/login/logout')
        assert response.status_code == 302
        assert b"Logged out" in response.data
