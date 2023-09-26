from django.urls import path
from patient.views import CreatePatientView


urlpatterns = [
    path('/', CreatePatientView.as_view(), name='Add new patients record'),
]