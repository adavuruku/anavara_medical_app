from django.urls import path
from medical_record.views import CreateMedicalRecordView, RetrieveAUserAllMedicalRecord,UpdateUserMedicalRecord, RetrieveAUserMedicalRecord


urlpatterns = [
    path('', CreateMedicalRecordView.as_view(), name='add_new_medical_record'),
    path('<int:medical_record_id>', UpdateUserMedicalRecord.as_view(), name='update_user_medical_record'),
    path('get/<int:medical_record_id>', RetrieveAUserMedicalRecord.as_view(), name='get_patient_single_medical_record'),
    path('get/all/<str:hospital_id>', RetrieveAUserAllMedicalRecord.as_view(), name='retrieve_patients_all_record'),
]