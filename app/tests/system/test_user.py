import json
import os
from api import load
from flask import jsonify
from api.models import User
from ..base_test import BaseTest
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies


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
                self.assertEqual(response.request.path, '/login/register')

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', data={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                auth_response = client.post('/login', data=json.dumps({
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                }), content_type='application/json')

                print(auth_response)

                # TODO: Test that access/csrf token is in response
                self.assertIn('access_token',
                              auth_response.content_type)

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/login/register', data={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })
                response = client.post('/login/register', data={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                self.assertDictEqual(
                    {'error': 'Email is already in use'}, json.loads(response.data))
