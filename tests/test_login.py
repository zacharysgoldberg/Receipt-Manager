from app.api import create_app
from app.api.models.models import User, db
from werkzeug.security import generate_password_hash


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
    app.app_context().push()
    user = User(
        firstname='Firstname',
        lastname='Lastname',
        email='admin@gmail.com',
        password=generate_password_hash('admin123'),
        authenticated=False
    )
    db.session.add(user)
    db.session.commit()
    with app.test_client() as client:
        response = client.post(
            '/login', json={'email': 'admin@gmail.com', 'password': 'admin123', 'remember': True}, content_type='application/json')
        assert response.status_code == 200
        assert b", logged in Succesfully" in response.data

    user = User.query.get_or_404(db.session.query(
        User.id).filter(User.email == 'admin@gmail.com').first()[0])
    db.session.delete(user)
    db.session.commit()

# test logout


def test_logout():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/login/logged_out')
        assert response.status_code == 302
        assert b"/login" in response.data
