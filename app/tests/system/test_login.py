from ..base_test import BaseTest


class TestHome(BaseTest):
    def test_home(self):
        with self.app() as client:
            response = client.get('/')

            self.assertEqual(response.status_code, 200)
