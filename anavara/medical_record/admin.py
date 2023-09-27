from django.contrib import admin

from django.contrib import admin
from medical_record.models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    pass