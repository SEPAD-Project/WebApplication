from django.db import models
import uuid
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
    
    schools = models.ManyToManyField(
        School,
        through='TeacherSchool',
        through_fields=('teacher_id', 'school_id'),
        related_name="teachers"
    )
    classes = models.ManyToManyField(
        Class,
        through='TeacherClass',
        through_fields=('teacher_id', 'class_id'),
        related_name="teachers"
    )
    
    def __str__(self):
        return f"{self.teacher_name} {self.teacher_family}"
    
class TeacherSchool(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'teacher_school'

class TeacherClass(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE) 
    
    class Meta:
        db_table = 'teacher_class'
