from datetime import date
from rest_framework import serializers

from users.serializers import UserSerializer
from patient.serializers import PatientSerializer
from .models import MedicalRecord
from patient.models import Patient
from django.core.exceptions import ValidationError
    
def treatment_date_in_the_past(value):
    today = date.today()
    if value < today:
        raise ValidationError('Treatment date cannot be in the past.')
        
class MedicalRecordUpdateBodySerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    class Meta:
        model = MedicalRecord
        fields = [
            'diagnosis',
            'treatment',
            'treatment_date',
        ]

class MedicalRecordBodySerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    patient_id = serializers.IntegerField()
    class Meta:
        model = MedicalRecord
        fields = [
            'diagnosis',
            'treatment',
            'treatment_date',
            'patient_id',
        ]
        extra_kwargs = {'patient_id': {'required': True},}

class  MedicalRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for Medical record model.
    """
    doctor = UserSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    treatment_date=serializers.DateField( validators=[treatment_date_in_the_past])
    patient_id = serializers.PrimaryKeyRelatedField(
        source='patient',
        queryset=Patient.objects.all()
    )
    class Meta:
        model = MedicalRecord
        fields = [
            'pk',
            'patient',
            'doctor',
            'diagnosis',
            'treatment',
            'treatment_date',
            'created_at',
            'patient_id',
            'is_deleted',
        ]