from rest_framework import generics
from rest_framework import status
from .models import Patient
from .serializers import PatientSerializer, PatientBodySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class CreatePatientView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientSerializer

    @swagger_auto_schema( request_body=PatientBodySerializer, operation_description='Create a patient')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save(created_by=self.request.user)
        # generate hospital_id for patient
        saved_id = 6 - len(str(patient.pk))
        newId = "0" * saved_id + str(patient.pk)
        patient.hospital_id = newId
        patient.save()
        return Response(PatientSerializer(patient).data, status=status.HTTP_200_OK)
        
    

# @receiver(post_save, sender=Patient)
# def my_handler(sender, **kwargs):
#     if sender.hospital_id is not None:
#         saved_id = 6 - len(str(sender.pk))
#         newId = "0" * saved_id + str(sender.pk)
#         # sender.hospital_id = newId
#         sender.objects.update(hospital_id = newId) # .save()