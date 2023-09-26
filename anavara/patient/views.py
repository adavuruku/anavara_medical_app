from django.shortcuts import render
from rest_framework import generics
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated


class CreatePatientView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)