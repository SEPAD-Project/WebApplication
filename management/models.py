from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# ---------------------- Custom User Manager ----------------------

class SchoolManager(BaseUserManager):
    def create_user(self, school_code, manager_personal_code, school_name, province, city, email):
        if not school_code or not manager_personal_code:
            raise ValueError('School code and manager personal code are required')
        user = self.model(
            school_code=school_code,
            manager_personal_code=manager_personal_code,
            school_name=school_name,
            province=province,
            city=city,
            email=email
        )
        user.set_password(manager_personal_code)
        user.save(using=self._db)
        return user

# ---------------------- School (Custom User) ----------------------

class School(AbstractBaseUser):
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

# ---------------------- Class ----------------------

class Class(models.Model):
    class_name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=100, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classes')

    def __str__(self):
        return self.class_name

# ---------------------- Teacher ----------------------

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=100)
    teacher_family = models.CharField(max_length=100)
    teacher_national_code = models.CharField(max_length=100, unique=True)
    teacher_password = models.CharField(max_length=100)
    lesson = models.CharField(max_length=100)

    classes = models.ManyToManyField(Class, related_name='teachers')
    schools = models.ManyToManyField(School, related_name='teachers')

    def __str__(self):
        return f"{self.teacher_name} {self.teacher_family}"

# ---------------------- Student ----------------------

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    student_family = models.CharField(max_length=100)
    student_national_code = models.CharField(max_length=100, unique=True)
    student_password = models.CharField(max_length=100)
    student_phone_number = models.CharField(max_length=100, unique=True)

    class_room = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='students')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')

    def __str__(self):
        return f"{self.student_name} {self.student_family}"
