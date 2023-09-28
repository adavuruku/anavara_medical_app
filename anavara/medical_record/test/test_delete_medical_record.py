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

    def test_delete_medical_record_successful(self):
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
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        
        medical_record_id = responseMed.json()['pk']

        responseMedDelete = client.delete(
            reverse('update_user_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedDelete.status_code, status.HTTP_204_NO_CONTENT)

        # fetching the record should return 404
        responseMedGet = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedGet.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertEqual(responseMedGet.json()['message'], 'Patient record doesnt exist')
    
    
    def test_doctor_delete_medical_record_created_by_another_doctor(self):
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
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        # create another doctor different from the doctor that creates the medical records
        responseStaff = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_two_payload),
            content_type='application/json'
        )
        # login the doctor and try to use its token to update record of doctor one
        responsestafflogin = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_two_login),
            content_type='application/json'
        )

        tokenDocTwo =responsestafflogin.json()['access']

        
        medical_record_id = responseMed.json()['pk']
        responseMedDelete = client.delete(
            reverse('update_user_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {tokenDocTwo}'}
        )
        self.assertEqual(responseMedDelete.status_code, status.HTTP_404_NOT_FOUND)

        # fetching the record should return 200 - since is not deleted
        responseMedGet = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedGet.status_code, status.HTTP_200_OK)

    def test_unauthorised_invalid_token_delete_medical_record(self):
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
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        badToken =responsetwo.json()['access']+'invalid_token'
        medical_record_id = responseMed.json()['pk']
        responseMedDelete = client.delete(
            reverse('update_user_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {badToken}'}
        )
        self.assertEqual(responseMedDelete.status_code, status.HTTP_401_UNAUTHORIZED)

        # fetching the record should return 200 - since is not deleted
        responseMedGet = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedGet.status_code, status.HTTP_200_OK)

        # WITH NO token at all
        responseMedDelete = client.delete(
            reverse('update_user_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json'
        )
        self.assertEqual(responseMedDelete.status_code, status.HTTP_401_UNAUTHORIZED)

        # fetching the record should return 200 - since is not deleted
        responseMedGet = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedGet.status_code, status.HTTP_200_OK)

    
    def test_doctor_delete_medical_record_created_by_another_doctor(self):
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
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        # create another doctor different from the doctor that creates the medical records
        responseStaff = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_doctor_two_payload),
            content_type='application/json'
        )
        # login the doctor and try to use its token to update record of doctor one
        responsestafflogin = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_doctor_two_login),
            content_type='application/json'
        )

        tokenDocTwo =responsestafflogin.json()['access']

        
        medical_record_id = responseMed.json()['pk']
        responseMedDelete = client.delete(
            reverse('update_user_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {tokenDocTwo}'}
        )
        self.assertEqual(responseMedDelete.status_code, status.HTTP_404_NOT_FOUND)

        # fetching the record should return 200 - since is not deleted
        responseMedGet = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedGet.status_code, status.HTTP_200_OK)

    
    def test_staff_user_deleting_record(self):
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
        self.valid_create_medical_record_payload['patient_id'] = responsePatient.json()['pk']
        responseMed = client.post(
            reverse('add_new_medical_record'),
            data=json.dumps(self.valid_create_medical_record_payload,indent=4, sort_keys=True, default=str),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )

        # create a staff user
        responseStaff = client.post(
            reverse('user_register'),
            data=json.dumps(self.valid_staff_payload),
            content_type='application/json'
        )
        # login the doctor and try to use its token to update record of doctor one
        responsestafflogin = client.post(
            reverse('token_obtain_pair'),
            data=json.dumps(self.valid_staff_login),
            content_type='application/json'
        )

        tokenDocTwo =responsestafflogin.json()['access']

        
        medical_record_id = responseMed.json()['pk']
        responseMedDelete = client.delete(
            reverse('update_user_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {tokenDocTwo}'}
        )
        self.assertEqual(responseMedDelete.status_code, status.HTTP_403_FORBIDDEN)

        # fetching the record should return 200 - since is not deleted
        responseMedGet = client.get(
            reverse('get_patient_single_medical_record', kwargs={'medical_record_id':medical_record_id}),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        self.assertEqual(responseMedGet.status_code, status.HTTP_200_OK)