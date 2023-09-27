from django.urls import path
from patient.views import CreatePatientView


urlpatterns = [
    path('', CreatePatientView.as_view(), name='add_new_patients_record'),
]