from django.db import models

from schools.models import School
from classes.models import Class

class Student(models.Model):
    class Meta:
        db_table = 'students'

    student_name = models.CharField(max_length=100)
    student_family = models.CharField(max_length=100)
    student_national_code = models.CharField(max_length=100, unique=True)
    student_password = models.CharField(max_length=100)
    student_phone_number = models.CharField(max_length=100, unique=True)

    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.student_name} {self.student_family}"
