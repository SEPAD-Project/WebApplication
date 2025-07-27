from django.db import models

from schools.models import School

class Class(models.Model):
    class Meta:
        db_table = 'classes'

    class_name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=100, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.class_name