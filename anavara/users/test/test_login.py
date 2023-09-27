# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase, Client
from ..models import User
import datetime
import json

import logging
logger = logging.getLogger(__name__)
# initialize the APIClient app
client = Client()

class UserViewSetTests(TestCase):

    def setUp(self):
        self.valid_payload = {
            "password": "test01",
            "email": "testcreate@example.com",
            "first_name": "Hadi",
            "last_name": "Hans",
            "confirm_password": "test01",
            "is_doctor": True
        }

        self.valid_login = {
            "password": "test01",
            "email": "testcreate@example.com"
        }
        self.invalid_login_password = {
            "password": "Mikey4000",
            "email": "testcreate@example.com"
        }
        self.invalid_login_email= {
            "password": "test01",
            "email": "testcreaterec@example.com"
        }
    def test_create_valid_login(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        self.assertTrue(response.json()['refresh'])
        self.assertTrue(response.json()['access'])

    def test_create_invalid_login_password(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.invalid_login_password),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.json()['detail'])
    
    def test_create_invalid_login_password(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        response = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.invalid_login_email),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(response.json()['detail'])