from django.contrib import admin

from django.contrib import admin
from patient.models import Patient

@admin.register(Patient)
class UserAdmin(admin.ModelAdmin):
    pass

