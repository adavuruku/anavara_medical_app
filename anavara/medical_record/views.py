from rest_framework import generics
from .models import MedicalRecord
from patient.models import Patient
from .serializers import MedicalRecordSerializer, MedicalRecordBodySerializer, MedicalRecordUpdateBodySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from .permission import MedicalRecordPermission
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer
from patient.serializers import PatientSerializer
from .pagination import CustomPagination


class CreateMedicalRecordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, MedicalRecordPermission)
    # queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    @swagger_auto_schema( request_body=MedicalRecordBodySerializer, operation_description='Create a patient medical record')
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medical_record = serializer.save(doctor=request.user, patient_id = request.data["patient_id"])
        return Response(MedicalRecordSerializer(medical_record).data, status=status.HTTP_200_OK)
    

class RetrieveAUserAllMedicalRecord(generics.ListAPIView):
    permission_classes = (IsAuthenticated,MedicalRecordPermission)
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    pagination_class = CustomPagination

    @swagger_auto_schema(operation_description='Retrieve a list of patient medical record')
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,  status=status.HTTP_200_OK)
    
    def get_queryset(self):
        patient = get_object_or_404(Patient, hospital_id= self.kwargs.get('hospital_id'))
        user_record = UserSerializer(self.request.user).data
        patient_record = PatientSerializer(patient).data
        qs = super().get_queryset()
        record = []
        if self.request.user.is_superuser:
            record = qs.filter(patient_id=patient_record["pk"], is_deleted= False)
        
        if user_record["is_doctor"]:
            record = qs.filter(patient_id=patient_record["pk"], doctor = self.request.user, is_deleted= False)
        return record
        

class UpdateUserMedicalRecord(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, MedicalRecordPermission)
    serializer_class = MedicalRecordSerializer

    def get_object(self, pk):
        medical_record = None
        user_record = UserSerializer(self.request.user).data
        if self.request.user.is_superuser:
            medical_record = get_object_or_404(MedicalRecord, pk=pk, is_deleted= False)
        if user_record["is_doctor"]:
            medical_record = get_object_or_404(MedicalRecord, pk=pk, doctor = self.request.user, is_deleted= False)
        return medical_record

    @swagger_auto_schema( request_body=MedicalRecordUpdateBodySerializer, operation_description='Update a patient medical record')
    def patch(self, request, *args, **kwargs):
        medical_record = self.get_object(self.kwargs.get('medical_record_id'))
        serializer = self.get_serializer(medical_record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        medical_record = serializer.save()
        return Response(MedicalRecordSerializer(medical_record).data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        medical_record = self.get_object(self.kwargs.get('medical_record_id'))
        serializer = self.get_serializer(medical_record, data= {"is_deleted": True}, partial=True)
        serializer.is_valid(raise_exception=True)
        medical_record = serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class RetrieveAUserMedicalRecord(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,MedicalRecordPermission)
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    @swagger_auto_schema(operation_description='Retrieve a patient medical record')
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data,  status=status.HTTP_200_OK)
    
    def get_queryset(self):
        user_record = UserSerializer(self.request.user).data
        # qs = super().get_queryset()
        record = None
        if self.request.user.is_superuser:
            record = get_object_or_404(MedicalRecord, pk=self.kwargs.get('medical_record_id'), is_deleted= False)
            # record = qs.filter(pk=self.kwargs.get('medical_record_id'), is_deleted= False)
        if user_record["is_doctor"]:
            record = get_object_or_404(MedicalRecord, pk=self.kwargs.get('medical_record_id'), doctor = self.request.user, is_deleted= False)
            # record = qs.filter(pk=self.kwargs.get('medical_record_id'), doctor = self.request.user, is_deleted= False)
        return record