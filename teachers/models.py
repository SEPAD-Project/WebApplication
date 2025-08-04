from django.db import models
import uuid
from schools.models import School
from classes.models import Class

class Teacher(models.Model):
    class Meta:
        db_table = 'teachers'
    
    teacher_name = models.CharField(max_length=100, db_column='teacher_name')
    teacher_family = models.CharField(max_length=100, db_column='teacher_family')
    teacher_national_code = models.CharField(max_length=100, unique=True, db_column='teacher_national_code')
    teacher_password = models.CharField(max_length=100, db_column='teacher_password')
    lesson = models.CharField(max_length=100, db_column='lesson')
    
    schools = models.ManyToManyField(
        School,
        through='TeacherSchool',
        through_fields=('teacher', 'school'),
        related_name="teachers"
    )

    classes = models.ManyToManyField(
        Class,
        through='TeacherClass',
        through_fields=('teacher', 'cls'),
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
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id')
    school = models.ForeignKey(School, on_delete=models.CASCADE, db_column='school_id')
    
    class Meta:
        db_table = 'teacher_school'

class TeacherClass(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, db_column='teacher_id')
    cls = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id')

    class Meta:
        db_table = 'teacher_class'
