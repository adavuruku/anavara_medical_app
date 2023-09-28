# Create your tests here.
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase, Client
from datetime import date, timedelta
import json

import logging
logger = logging.getLogger(__name__)
# initialize the APIClient app
client = Client()
token = None
today = date.today()
past_day = today - timedelta(days=10)
class MedicalRecordViewSetTests(TestCase):

    def setUp(self):
        self.valid_doctor_payload = {
            "password": "test01",
            "email": "testcreate@example.com",
            "first_name": "Hadi",
            "last_name": "Hans",
            "confirm_password": "test01",
            "is_doctor": True
        }

        self.valid_staff_user_payload = {
            "password": "test01",
            "email": "testcreatestaff@example.com",
            "first_name": "Muibat",
            "last_name": "Ojo",
            "confirm_password": "test01",
            "is_doctor": False
        }

        self.valid_doctor_login = {
           "password": "test01",
            "email": "testcreate@example.com"
        }

        self.valid_staff_login = {
           "password": "test01",
            "email": "testcreatestaff@example.com"
        }
        self.create_patient_payload = {
            "first_name": "Joseph",
            "last_name": "Conan",
            "phone_number": "+2348164377187",
            "email_address": "user@example.com",
            "address": "Monaco street abuja",
            "gender": "Male"
        }

        self.valid_create_medical_record_payload = {
            "diagnosis": "Lorem Ipsum loresita meta mata artum",
            "treatment": "Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum",
            "treatment_date": today,
            "patient_id": 1
        }

        self.valid_create_medical__invalid_payload_past_date = {
            "diagnosis": "Lorem Ipsum loresita meta mata artum",
            "treatment": "Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum",
            "treatment_date": past_day,
            "patient_id": 1
        }

        self.valid_create_medical__invalid_payload_patient_not_exist = {
            "diagnosis": "Lorem Ipsum loresita meta mata artum",
            "treatment": "Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum",
            "treatment_date": today,
            "patient_id": 50
        }
        self.create_patient_payload_invalid_field_not_exist = {
            "treatment": "Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum Lorem Ipsum loresita meta mata artum",
            "treatment_date": today,
            "patient_id": 1
        }
    
    def test_create_valid_medical_record(self):
        # create a doctor
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_payload),
            content_type='application/json'
        )
        # login a doctor
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_login),
            content_type='application/json'
        )

        token =responsetwo.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            # json date serialisation issue https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
            # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMed.status_code, status.HTTP_200_OK)
    
    def test_create_medical_record_past_date(self):
        # create a doctor
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_payload),
            content_type='application/json'
        )
        # login a doctor
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_login),
            content_type='application/json'
        )

        token =responsetwo.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.valid_create_medical__invalid_payload_past_date['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical__invalid_payload_past_date,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMed.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_medical_record_patient_invalid_patient_id(self):
        # create a doctor
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_payload),
            content_type='application/json'
        )
        # login a doctor
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_login),
            content_type='application/json'
        )

        token =responsetwo.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.valid_create_medical__invalid_payload_patient_not_exist['patient_id'] = responsePatient.json()['pk'] + 30
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical__invalid_payload_patient_not_exist,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMed.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_medical_record_invalid_payload(self):
        # create a doctor
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_payload),
            content_type='application/json'
        )
        # login a doctor
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_login),
            content_type='application/json'
        )

        token =responsetwo.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.create_patient_payload_invalid_field_not_exist['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.create_patient_payload_invalid_field_not_exist,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMed.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_medical_record_by_user_with_no_doctor_or_super_user_access(self):
        # create a doctor
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_staff_user_payload),
            content_type='application/json'
        )
        # login a doctor
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_staff_login),
            content_type='application/json'
        )

        token =responsetwo.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMed.status_code, status.HTTP_403_FORBIDDEN)