from dotenv import load_dotenv
import os

load_dotenv()

# test user table


def test_new_user(new_user):
    email = 'admin@domain.com'
    assert new_user.firstname == 'Firstname'
    assert new_user.lastname == 'Lastname'
    assert new_user.email == email
    assert new_user.password == os.getenv('SEED_PASS')
    assert new_user.username == email.split('@')[0]
