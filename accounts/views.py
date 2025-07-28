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
            return redirect('')
        return redirect('error_unknown_school')

    return render(request, 'form/login.html')


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
            return redirect('error_duplicate_school')

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

        return redirect('success_registration')

    return render(request, 'form/signup.html')


# View for duplicate school registration error
def duplicate_school_error_view(request):
    return render(request, 'error/duplicated_school_info.html')


# View to notify user of their username and password after registration
def registration_success_view(request):
    return render(request, 'error/notify_username_password.html')


# View for unknown school info error during login
def unknown_school_error_view(request):
    return render(request, 'error/unknown_school_info.html')
