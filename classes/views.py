from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from .models import Class
from utils.excel_reading import add_classes
from utils.generate_class_code import generate_class_code


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

def remove_class(request, class_name):
    current_user = request.user

    cls = Class.objects.filter(Q(class_name=class_name)&Q(school=current_user.id)).first()
    if cls is None:
        return redirect('unknown_student_info')

    Class.delete(cls)
        
    return redirect('classes')

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