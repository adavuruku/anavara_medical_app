from django.urls import path
from medical_record.views import CreateMedicalRecordView


urlpatterns = [
    path('', CreateMedicalRecordView.as_view(), name='Add new medical record'),
]