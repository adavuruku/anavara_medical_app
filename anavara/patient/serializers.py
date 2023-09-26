from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model.
    """
    # created_by = UserSerializer(source='user', write_only=True)
    created_by = serializers.SerializerMethodField('get_selected_city_name')
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
            'created_by':{'read_only': True},
            'gender': {'required': True},'last_name': {'required': True},
            'address': {'required': True},'email_address': {'required': False},
            'phone_number': {'required': True},'first_name': {'required': True},
        }