import os
from ..base_test import BaseTest
from api.models import User


class UserTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            user = User.create_user(email=os.getenv('ADMIN'),
                                    password=os.getenv('MAIL_PASSWORD'),
                                    access=2)

            self.assertIsNotNone(User.query.filter_by(username=user.username))
            self.assertIsNotNone(User.query.filter_by(_id=user._id))
