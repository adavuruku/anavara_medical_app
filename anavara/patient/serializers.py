from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Patient

class PatientBodySerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    class Meta:
        model = Patient
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email_address',
            'address',
            'gender',
        ]

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    created_by = UserSerializer(read_only=True)
    # created_by = serializers.SerializerMethodField('get_created_by')
    class Meta:
        model = Patient
        fields = [
            'pk',
            'created_by',
            'first_name',
            'last_name',
            'phone_number',
            'email_address',
            'address',
            'gender',
            'created_at',
            'hospital_id',
        ]
        extra_kwargs = {
            'hospital_id': {'read_only': True},
        }
    
    # def get_created_by(self, obj):
    #     return UserSerializer(obj.created_by).data
