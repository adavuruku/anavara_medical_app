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
test_url = 'http://127.0.0.1:8081/user/register'
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
        self.invalid_password_payload = {
            "password": "Hadi001",
            "email": "testcreate2@example.com",
            "first_name": "Hadi001",
            "last_name": "Hadi001",
            "confirm_password": "Hadi001",
            "is_doctor": True
        }

        self.invalid_confirm_password_payload = {
            "password": "Mikey40",
            "email": "testcreate3@example.com",
            "first_name": "Hadi",
            "last_name": "Hans",
            "confirm_password": "Mikey30",
            "is_doctor": True
        }

        self.invalid_duplicate_email_payload = {
            "password": "Mikey40",
            "email": "testcreate@example.com",
            "first_name": "Hadi",
            "last_name": "Hans",
            "confirm_password": "Mikey40",
            "is_doctor": True
        }

    def test_create_valid_user(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_email(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.invalid_duplicate_email_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_invalid_confirm_password(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.invalid_confirm_password_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

   