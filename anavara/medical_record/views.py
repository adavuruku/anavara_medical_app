from rest_framework import generics
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer, MedicalRecordBodySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .permission import CanCreateMedicalRecord


class CreateMedicalRecordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, CanCreateMedicalRecord)
    # queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    @swagger_auto_schema( request_body=MedicalRecordBodySerializer, operation_description='Create a patient medical record')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medical_record = serializer.save(doctor=request.user, patient_id = request.data["patient_id"])
        return Response(MedicalRecordSerializer(medical_record).data, status=status.HTTP_200_OK)
    

class RetrieveAUserMedicalRecord(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    # queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    @swagger_auto_schema( request_body=MedicalRecordBodySerializer, operation_description='Create a patient medical record')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medical_record = serializer.save(doctor=request.user, patient_id = request.data["patient_id"])
        return Response(MedicalRecordSerializer(medical_record).data, status=status.HTTP_200_OK)