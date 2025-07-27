from django.contrib.auth.models import BaseUserManager

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