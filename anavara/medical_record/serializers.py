from rest_framework import serializers

from users.serializers import UserSerializer
from patient.serializers import PatientSerializer
from .models import MedicalRecord
from patient.models import Patient

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
        ]