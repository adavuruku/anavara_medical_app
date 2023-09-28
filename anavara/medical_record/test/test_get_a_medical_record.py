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
        self.valid_doctor_one_payload = {
            "password": "test01",
            "email": "testcreate@example.com",
            "first_name": "Hadi",
            "last_name": "Hans",
            "confirm_password": "test01",
            "is_doctor": True
        }

        self.valid_doctor_two_payload = {
            "password": "test01",
            "email": "testcreatestaff@example.com",
            "first_name": "Muibat",
            "last_name": "Ojo",
            "confirm_password": "test01",
            "is_doctor": True
        }

        self.valid_staff_payload = {
            "password": "test01",
            "email": "realstaff@example.com",
            "first_name": "Okoro",
            "last_name": "Manna",
            "confirm_password": "test01",
            "is_doctor": False
        }

        self.valid_doctor_one_login = {
           "password": "test01",
            "email": "testcreate@example.com"
        }

        self.valid_doctor_two_login = {
           "password": "test01",
            "email": "testcreatestaff@example.com"
        }
        self.valid_staff_login= {
            "password": "test01",
            "email": "realstaff@example.com"
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

    def test_medical_record_created_by_doctor_one(self):
        # create a doctor
        responseOne = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_one_payload),
            content_type='application/json'
        )
        # login a doctor
        responsetwo = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_one_login),
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

        # create medical record for user
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        medical_record_id = responseMed.json()['pk']
        responseList = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id': medical_record_id}),
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseList.status_code, status.HTTP_200_OK)
        self.assertEqual(responseList.data['pk'], medical_record_id)

    def test_doctor_can_only_access_medical_record_he_created(self):
        # create doctor one
        doctor_one = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_one_payload),
            content_type='application/json'
        )
        # login doctor one
        doctor_one_login = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_one_login),
            content_type='application/json'
        )

        token =doctor_one_login.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        

        # create medical record for user
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        medical_record_id = responseMed.json()['pk']
        # create doctor two
        doctor_two = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_two_payload),
            content_type='application/json'
        )
        # login doctor two
        doctor_two_login = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_two_login),
            content_type='application/json'
        )

        token = doctor_two_login.json()['access']

        responseList = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id': medical_record_id}),
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseList.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_user_cannot_access_any_medical_record(self):
        # create doctor one
        doctor_one = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_one_payload),
            content_type='application/json'
        )
        # login doctor one
        doctor_one_login = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_one_login),
            content_type='application/json'
        )

        token =doctor_one_login.json()['access']

        # create staff user and use the record to create a patient
        staff_record = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_staff_payload),
            content_type='application/json'
        )
        # login staff user to get token
        staff_login = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_staff_login),
            content_type='application/json'
        )

        staff_token = staff_login.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {staff_token}'}
        )
        

        # create medical record for user [use doctor token]
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        # doctor one create two record medical record
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        responseMed2 = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        medical_record_id = responseMed2.json()['pk']
        responseList = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id': medical_record_id}),
            **{'HTTP_AUTHORIZATION': f'Bearer {staff_token}'}
        )
        self.assertEqual(responseList.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_medical_record_with_invalid_token(self):
        # create doctor one
        doctor_one = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_one_payload),
            content_type='application/json'
        )
        # login doctor one
        doctor_one_login = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_one_login),
            content_type='application/json'
        )

        token =doctor_one_login.json()['access']

        # create a patient
        responsePatient = client.post(
            reverse('add_new_patients_record'),
            data=json.dumps(self.create_patient_payload),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        

        # create medical record for user [use doctor token]
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        # doctor one create a record medical record
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        medical_record_id = responseMed.json()['pk']
        token = token + 'invalid'
        responseList = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id': medical_record_id}),
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseList.status_code, status.HTTP_401_UNAUTHORIZED)

        responseListNoToken = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id': medical_record_id})
        )
        self.assertEqual(responseListNoToken.status_code, status.HTTP_401_UNAUTHORIZED)