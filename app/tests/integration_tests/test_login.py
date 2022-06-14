from .base_test import BaseTest


class TestHome(BaseTest):
    def test_home(self):
        with self.app as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 200)
