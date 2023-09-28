# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase, Client
import datetime
import json

import logging
logger = logging.getLogger(__name__)
# initialize the APIClient app
client = Client()
token = None
class PatientViewSetTests(TestCase):

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
        self.valid_create_patient_payload = {
            "first_name": "Joseph",
            "last_name": "Conan",
            "phone_number": "+2348164377187",
            "email_address": "user@example.com",
            "address": "Monaco street abuja",
            "gender": "Male"
        }

        self.create_patient_payload_invalid_phone_number = {
            "first_name": "Joseph",
            "last_name": "Conan",
            "phone_number": "08164377187",
            "email_address": "user@example.com",
            "address": "Monaco street abuja",
            "gender": "Male"
        }
        self.create_patient_payload_invalid_email_address = {
            "first_name": "Joseph",
            "last_name": "Conan",
            "phone_number": "08164377187",
            "email_address": "user@example.com",
            "address": "Monaco street abuja",
            "gender": "Male"
        }

        self.create_patient_payload_invalid_gender = {
            "first_name": "Joseph",
            "last_name": "Conan",
            "phone_number": "08164377187",
            "email_address": "user@example.com",
            "address": "Monaco street abuja",
            "gender": "Woman"
        }

        self.create_patient_payload_invalid_missing_field = {
            "last_name": "Conan",
            "phone_number": "08164377187",
            "email_address": "user@example.com",
            "address": "Monaco street abuja",
            "gender": "Male"
        }

    def test_create_valid_patient_record(self):
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

        token =responsetwo.json()['access']
        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.valid_create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_patient_record_without_auth_invalid_auth(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.valid_create_patient_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.valid_create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}grr'}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_invalid_patient_record_phone_number(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        token =responsetwo.json()['access']
        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload_invalid_phone_number),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_patient_record_email_address(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        token =responsetwo.json()['access']
        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload_invalid_email_address),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_patient_record_gender_and_missing_field(self):
        response = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )

        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        token =responsetwo.json()['access']
        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload_invalid_gender),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload_invalid_missing_field),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        