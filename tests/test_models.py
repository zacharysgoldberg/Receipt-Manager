from dotenv import load_dotenv
import os

load_dotenv()

# test user table


def test_new_user(new_user):

    assert new_user.firstname == 'Firstname'
    assert new_user.lastname == 'Lastname'
    assert new_user.email == 'admin@domain.com'
    assert new_user.password == os.getenv('seed_pass')
    assert new_user.authenticated == False
