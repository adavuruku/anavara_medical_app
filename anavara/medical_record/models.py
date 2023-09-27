from django.db import models
from patient.models import Patient
from users.models import User
from django.conf import settings

# Create your models here.

class MedicalRecord(models.Model):
    diagnosis = models.TextField()
    treatment = models.TextField()
    doctor = models.ForeignKey(to=settings.AUTH_USER_MODEL,related_name='registered_medical_record', on_delete=models.PROTECT)
    patient = models.ForeignKey(to=Patient,related_name='my_medical_record', on_delete=models.PROTECT)
    treatment_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = False
        verbose_name = "Search Medical record"
        verbose_name_plural = "Search Medical record"
        # rules_permissions = Perms.all_is_staff
        ordering: ['-updated_at', 'doctor', 'patient']
