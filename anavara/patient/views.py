from django.shortcuts import render
from rest_framework import generics
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated

from django.db.models.signals import post_save
from django.dispatch import receiver


class CreatePatientView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
    

@receiver(post_save, sender=Patient)
def my_handler(sender, **kwargs):
    if sender.hospital_id is not None:
        saved_id = 6 - len(str(sender.pk))
        newId = "0" * saved_id + str(sender.pk)
        # sender.hospital_id = newId
        sender.objects.update(hospital_id = newId) # .save()