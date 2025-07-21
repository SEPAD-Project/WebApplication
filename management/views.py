from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from .models import School, Class
from utils.excel_reading import add_classes
from utils.generate_class_code import generate_class_code

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
    if request.method == 'POST':
        class_name = request.POST.get('class_name')

        current_user = request.user
        school_code = current_user.school_code

        class_code=generate_class_code(school_code, class_name)
        if Class.objects.filter(class_code=class_code):
            return redirect('duplicated_class_info')
        
        Class.objects.create(class_name=class_name, 
                            class_code=class_code,
                            school=current_user)
        
        return redirect('classes')

    return render(request, 'add_class.html')

@login_required
def add_classes_from_excel(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        sheet_name = request.POST.get('sheet')
        name_letter = request.POST.get('name')

        classes = Class.objects.all()
        school_user = request.user

        result = add_classes(filename, sheet_name, name_letter, [cls.class_name for cls in classes], school_user.school_code)
        
        if result == 'sheet_not_found':
            return redirect('error_in_class_excel')

        if result == 'bad_column_letter':
            return redirect('error_in_class_excel')

        if isinstance(result[0], list):
            return redirect('error_in_class_excel')
        
        for cls in result:
            Class.objects.create(
                class_name=cls['name'],
                class_code=cls['code'],
                school_id=school_user.id,
            )

        return redirect('classes')

    return render(request, 'add_classes_from_excel.html')

@login_required
def class_info(request, class_name):
    current_user  = request.user
    data = Class.objects.filter(Q(class_name=class_name) & Q(school=current_user.id)).first()

    if data is None:
        return redirect(unknown_class_info)

    return render(request, 'class_info.html', {'data':data, 'teachers':data.teachers.all(), 'students':data.students.all()})

@login_required
def edit_class(request, class_name):
    current_user  = request.user
    data = Class.objects.filter(Q(class_name=class_name) & Q(school=current_user.id)).first()

    if data is None:
        return redirect(unknown_class_info)
    
    if request.method == 'POST':
        new_name = request.POST.get("class_name")

        if new_name==class_name:
            return redirect('classes')
        
        if Class.objects.filter(Q(class_name=new_name) & Q(school=current_user.id)):
            return redirect('duplicated_class_info')

        new_code = generate_class_code(current_user.school_code, new_name)

        data.class_name = new_name
        data.class_code = new_code
        data.save()

        return redirect('classes')


    return render(request, 'edit_class.html', {'name':data.class_name})

def duplicated_class_info(request):
    return render(request, 'duplicated_class_info.html')

def error_in_class_excel(request):
    return render(request, 'error_in_class_excel.html')

def class_file_permission_error(request):
    return render(request, 'class_file_permission_error.html')

def unknown_class_info(request):
    return render(request, 'unknown_class_info.html')

def error_in_schedule(request):
    return render(request, 'error_in_schedule.html')

def teachers(request):
    currect_user = request.user
    teachers = currect_user.teachers.all()
    return render(request, 'teachers.html', {'teachers':teachers})