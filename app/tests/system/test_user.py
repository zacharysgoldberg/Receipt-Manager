import json
import logging
import os
from api import load
from flask import jsonify
from api.models import User
from ..base_test import BaseTest, _get_cookie_from_response
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies
# from parameterized import parameterized_class


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/login/register', json={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                self.assertIsNotNone(
                    User.query.filter_by(email=os.getenv('ADMIN'))
                )
                self.assertEqual(response.request.path, '/login/register')

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():

                client.post('/login/register', data={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                response = client.post('/login', data={
                    'email': os.getenv('ADMIN'),
                    'password': os.getenv('MAIL_PASSWORD')
                })

                cookies = response.headers.getlist('Set-Cookie')
                self.assertEqual(len(cookies), 4)

                access_cookie = _get_cookie_from_response(
                    response, "access_token_cookie")
                self.assertIsNotNone(access_cookie)

                access_csrf_cookie = _get_cookie_from_response(
                    response, 'csrf_access_token')
                self.assertIsNotNone(access_csrf_cookie)

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
