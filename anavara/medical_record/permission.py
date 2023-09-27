from rest_framework import permissions
from users.serializers import UserSerializer

class MedicalRecordPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ('POST', 'GET', 'PATCH', 'DELETE'):
            user_record = UserSerializer(request.user).data
            if user_record["is_doctor"] or request.user.is_superuser:
                return True
        return False