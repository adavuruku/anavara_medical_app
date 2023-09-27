from rest_framework import permissions

class CanCreateMedicalRecord(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method =='POST':
            print(request.user)
        return False