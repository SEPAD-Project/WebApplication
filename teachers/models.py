from django.db import models

from schools.models import School
from classes.models import Class

class Teacher(models.Model):
    class Meta:
        db_table = 'teachers'

    teacher_name = models.CharField(max_length=100)
    teacher_family = models.CharField(max_length=100)
    teacher_national_code = models.CharField(max_length=100, unique=True)
    teacher_password = models.CharField(max_length=100)
    lesson = models.CharField(max_length=100)

    classes = models.ManyToManyField(Class, related_name='teachers')
    schools = models.ManyToManyField(School, related_name='teachers')

    def __str__(self):
        return f"{self.teacher_name} {self.teacher_family}"