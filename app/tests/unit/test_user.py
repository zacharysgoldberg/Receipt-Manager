from .unit_base_test import UnitBaseTest
from api.models import User


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = User('firstname',
                    'lastname',
                    'email@domain.com',
                    'password',
                    'email',
                    1)

        self.assertEqual(user.firstname, 'firstname')
        self.assertEqual(user.lastname, 'lastname')
        self.assertEqual(user.email, 'email@domain.com')
        self.assertEqual(user.password, 'password')
        self.assertEqual(user.username, 'email')
        self.assertEqual(user.access, 1)
