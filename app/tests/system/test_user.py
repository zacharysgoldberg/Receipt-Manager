import json
import os
from api import load
from api.models import User
from ..base_test import BaseTest


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                self.assertIsNotNone(
                    User.query.filter_by(email=os.getenv('ADMIN')))
                self.assertDictEqual(
                    {
                        'id': 1,
                        'firstname': None,
                        'lastname': None,
                        'email': os.getenv('ADMIN'),
                        'username': os.getenv('ADMIN').split('@')[0],
                        'access_level': 1
                    }, response.json)

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })
                auth_response = client.post('/login', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                }, headers={'Content-Type': 'application/json'})

                self.assertIn('access_csrf',
                              auth_response.json.keys())
                self.assertIn('refresh_csrf', auth_response.json.keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })
                response = client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                self.assertDictEqual(
                    {'error': 'Email is already in use'}, response.json)
