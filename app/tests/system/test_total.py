import os
from api.models import Total, User
from ..base_test import BaseTest


class TotalTest(BaseTest):
    def test_create_total(self):
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })
                response = client.post('/')

    def test_create_duplicate_total(self):
        pass

    def test_delete_total(self):
        pass

    def test_find_total(self):
        pass

    def test_total_not_found(self):
        pass

    def test_total_found_with_receipts(self):
        pass

    def test_total_list(self):
        pass

    def test_total_list_with_receipts(self):
        pass
