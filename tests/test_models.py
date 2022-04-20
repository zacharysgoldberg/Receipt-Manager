# testing user table

def test_new_user_with_fixture(new_user):

    assert new_user.firstname == 'Firstname'
    assert new_user.lastname == 'Lastname'
    assert new_user.email == 'admin@gmail.com'
    assert new_user.password == 'admin123'
