from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from .models import School

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def downloads(request):
    return render(request, 'downloads.html')

def contact(request):
    return render(request, 'contact.html')

def comings_soon(request):
    return render(request, 'coming_soon.html')

def page_404(request):
    return render(request, '404.html')

def page_429(request):
    return render(request, '429.html')

def login_view(request):
    if request.method == 'POST':
        school_code = request.POST.get('school_code')
        manager_personal_code = request.POST.get('manager_personal_code')

        user = authenticate(request, username=school_code, password=manager_personal_code)

        if user is not None:
            login(request, user)
            return redirect('notify_username_password')
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

@login_required
def panel_entry(request):
    return render(request, 'panel_entry.html')

@login_required
def school_info(request):
    current_user = request.user
    
    cc = len(current_user.classes.all())
    tc = len(current_user.teachers.all())
    sc = len(current_user.students.all())
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    return render(request, 'school_info.html', {'data':current_user, 'cc':cc, 'tc':tc, 'sc':sc})

@login_required
def classes(request):
    current_user = request.user
    classes = current_user.classes.all()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    return render(request, 'classes.html', {'classes':classes})

@login_required
def add_class(request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    return render(request, 'add_class.html')

