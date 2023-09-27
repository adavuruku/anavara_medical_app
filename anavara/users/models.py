from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from users.user_manager import UserManager;


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_doctor = models.BooleanField(verbose_name='Indicate if user is a doctor',default=False)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
