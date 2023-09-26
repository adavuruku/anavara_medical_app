from django.db import models
from users.models import User
from django.conf import settings

# Create your models here.


class Patient(models.Model):

    GENDER_OPTION = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    gender = models.CharField(choices=GENDER_OPTION, max_length=10)
    hospital_id = models.CharField(
           max_length = 10,
           blank=True,
           null= True,
           editable=False,
        #    unique=True,
        #    default=create_new_ref_number
      )
    first_name = models.CharField(null=False, blank=False, max_length=10)
    last_name = models.CharField(null=False, blank=False, max_length=10)
    phone_number = models.CharField(max_length=11)
    email_address = models.EmailField( max_length=10)
    address = models.TextField()
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL,related_name='registered_patients', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = False
        verbose_name = "Search Category"
        verbose_name_plural = "Search Categories"
        # rules_permissions = Perms.all_is_staff
        ordering: ['-updated_at', 'created_by', 'hospital_id']

    def __str__(self):
        return str(self.first_name)+'s record'
