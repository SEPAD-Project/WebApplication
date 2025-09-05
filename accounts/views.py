from django.contrib.auth import login
from django.db.models import Q
from django.shortcuts import redirect, render

from schools.models import School
from utils.server.Website.directory_manager import dm_create_school


# View for school login using school code and manager personal code
def school_login_view(request):
    if request.method == 'POST':
        school_code = request.POST.get('school_code')
        manager_code = request.POST.get('manager_personal_code')

        school_user = School.objects.filter(
            Q(school_code=school_code) & Q(manager_personal_code=manager_code)
        ).first()

        if school_user is not None:
            login(request, school_user)
            return redirect('schools:dashboard')
        return render(request, 'accounts/unknown_school_error.html')

    return render(request, 'accounts/school_login.html')


# View to handle school signup and user creation
def school_signup_view(request):
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        school_code = request.POST.get('school_code')
        manager_code = request.POST.get('manager_personal_code')
        province = request.POST.get('province')
        city = request.POST.get('city')
        email = request.POST.get('email')

        existing_school = School.objects.filter(
            Q(school_code=school_code) | Q(manager_personal_code=manager_code)
        )
        if existing_school.exists():
            return render(request, 'accounts/duplicate_school_error.html')

        new_school = School.objects.create_user(
            school_name=school_name,
            school_code=school_code,
            manager_personal_code=manager_code,
            province=province,
            city=city,
            email=email
        )

        # Create directory for new school
        dm_create_school(str(new_school.id))

        return render(request, 'accounts/registration_success.html')

    return render(request, 'accounts/school_signup.html')

