from django.db import models

from schools.models import School
from classes.models import Class

class Student(models.Model):
    class Meta:
        db_table = 'students'

    student_name = models.CharField(max_length=100, db_column='student_name')
    student_family = models.CharField(max_length=100, db_column='student_family')
    student_national_code = models.CharField(max_length=100, unique=True, db_column='student_national_code')
    student_password = models.CharField(max_length=100, db_column='student_password')
    student_phone_number = models.CharField(max_length=100, unique=True, db_column='student_phone_number')

    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students', db_column='class_id')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', db_column='school_id')

    def __str__(self):
        return f"{self.student_name} {self.student_family}"
