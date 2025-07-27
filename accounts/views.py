from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.db.models import Q

from schools.models import School

def login_view(request):
    if request.method == 'POST':
        school_code = request.POST.get('school_code')
        manager_personal_code = request.POST.get('manager_personal_code')

        user = School.objects.filter(Q(school_code=school_code)&Q(manager_personal_code=manager_personal_code)).first()
        print(user)

        if user is not None:
            login(request, user)
            return redirect('panel_entry')
        else:
            return redirect('unknown_school_info')
            
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        school_name = request.POST.get('school_name')
        school_code = request.POST.get('school_code')
        manager_personal_code = request.POST.get('manager_personal_code')
        province = request.POST.get('province')
        city = request.POST.get('city')
        email = request.POST.get('email')

        if School.objects.filter(Q(school_code=school_code) | Q(manager_personal_code=manager_personal_code)):
            return redirect('duplicated_school_info')

        School.objects.create_user(
            school_name=school_name,
            school_code=school_code,
            manager_personal_code=manager_personal_code,
            province=province,
            city=city,
            email=email
        )

        return redirect('notify_username_password')
    
    return render(request, 'signup.html')

def duplicated_school_info(request):
    return render(request, 'duplicated_school_info.html')

def notify_username_password(request):
    return render(request, 'notify_username_password.html')

def unknown_school_info(request):
    return render(request, 'unknown_school_info.html')