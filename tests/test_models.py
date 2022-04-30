from conftest import rand_int
# test user table


def test_new_user(new_user):

    assert new_user.firstname == 'Firstname'
    assert new_user.lastname == 'Lastname'
    assert new_user.email == f'admin{rand_int}@gmail.com'
    assert new_user.password == 'admin123'
    assert new_user.authenticated == False
