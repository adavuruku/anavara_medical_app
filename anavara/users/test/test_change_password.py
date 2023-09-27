# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase, Client
from ..models import User
import datetime
import json
import requests

import logging
logger = logging.getLogger(__name__)
# initialize the APIClient app
client = Client()
token = None
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
        self.invalid_change_password_payload = {
            "old_password": "Mikey40",
            "new_password": "Mikey40",
            "confirm_password": "Mikey40",
        }

        self.valid_change_password_payload = {
            "old_password": "test01",
            "new_password": "Mikey40",
            "confirm_password": "Mikey40",
        }

        # response = client.post(
        #     reverse('user_register'),
        #     data=json.dumps(self.valid_payload),
        #     content_type='application/json'
        # )

    def test_create_valid_change_password(self):
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        self.assertTrue(responsetwo.json()['refresh'])
        self.assertTrue(responsetwo.json()['access'])

        # client..Add("Authorization", "Bearer " + response.json()['access']);

        # headers = {'Authorization': 'Bearer ' + responsetwo.json()['access'],'content_type':'application/json',}

        token =responsetwo.json()['access']
        response = client.patch(
            reverse('user_change_password'),
            data=json.dumps(self.valid_change_password_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['refresh'])
        self.assertTrue(response.json()['access'])

    def test_create_valid_change_password_without_auth(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        response = client.post(
            reverse('user_change_password'),
            data=json.dumps(self.valid_change_password_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)