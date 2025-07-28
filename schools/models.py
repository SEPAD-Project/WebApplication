from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from accounts.models import SchoolManager

class School(AbstractBaseUser):
    class Meta:
        db_table = 'schools'

    school_code = models.CharField(max_length=100, unique=True)
    manager_personal_code = models.CharField(max_length=100, unique=True)
    school_name = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    objects = SchoolManager()

    USERNAME_FIELD = 'school_code'
    REQUIRED_FIELDS = ['manager_personal_code', 'school_name', 'province', 'city', 'email']

    def __str__(self):
        return self.school_name