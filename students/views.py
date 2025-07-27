from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.files.storage import FileSystemStorage

from .models import Student
from classes.models import Class

from utils.excel_reading import add_students
from utils.server.Website.directory_manager import dm_create_student, dm_edit_student, dm_delete_student


def students(request):
    currect_user = request.user
    students = currect_user.students.all()
    return render(request, 'main/students.html', {'students':students})

def add_student(request):
    current_user = request.user
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_family = request.POST.get('student_family')
        student_national_code = request.POST.get('student_national_code')
        student_password = request.POST.get('student_password')
        student_phone_number = request.POST.get('student_phone_number')

        selected_class_code = request.POST.get('selected_class')

        if Student.objects.filter(Q(student_national_code=student_national_code) | Q(student_phone_number=student_phone_number)):
            return redirect('add_student')
        
        student_class = Class.objects.get(id=int(selected_class_code))
        Student.objects.create(student_name=student_name,
                               student_family=student_family,
                               student_national_code=student_national_code,
                               student_password=student_password,
                               student_phone_number=student_phone_number,
                               student_class=student_class,
                               school=current_user)
        
        dm_create_student(school_id=str(current_user.id), class_id=str(student_class.id), student_code=student_national_code)
        
        return redirect('students')

    return render(request, 'form/add_student.html', {'classes':current_user.classes.all()})

def duplicated_student_info(request):
    return render(request, 'error/duplicated_student_info.html')

def error_in_student_excel(request):
    return render(request, 'error/error_in_student_excel.html')

def student_file_permission_error(request):
    return render(request, 'error/student_file_permission_error.html')

def unknown_student_info(request):
    return render(request, 'error/unknown_student_info.html')

@login_required
def add_students_from_excel(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        sheet_name = request.POST.get('sheet')
        name_letter = request.POST.get('name')
        family_letter = request.POST.get('family')
        nc_letter = request.POST.get('national_code')
        class_letter = request.POST.get('class')
        pass_letter = request.POST.get('password')
        phone_letter = request.POST.get('phone_number')

        classes = Class.objects.all()
        students = Student.objects.all()
        school_user = request.user

        result = add_students(filename, sheet_name, name_letter, family_letter, nc_letter, class_letter, pass_letter, phone_letter,
                              [cls.class_name for cls in classes],
                              [student.student_national_code for student in students],
                              [student.student_phone_number for student in students],
                              school_user.school_code)
        
        if result == 'sheet_not_found':
            return redirect('error_in_student_excel')

        if result == 'bad_column_letter':
            return redirect('error_in_student_excel')
        
        if isinstance(result[0], list):
            excel_errors = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    excel_errors.append(f"Bad data format in cell {cell}.")
                elif problem[0] == "duplicated_nc":
                    excel_errors.append(
                        f"Duplicated national code in cell {cell}.")
                elif problem[0] == 'unknown_class':
                    excel_errors.append(f"Unknown class name in cell {cell}.")
                else:
                    excel_errors.append(f"Unknown issue in cell {cell}.")

            return redirect('error_in_student_excel')
        
        for student in result:
            cls = Class.objects.filter(class_code=student['class']).first()
            Student.objects.create(
                student_name=student['name'],
                student_family=student['family'],
                student_national_code=student['national_code'],
                student_phone_number=student['phone_number'],
                student_class=cls,
                student_password=student['password'],
                school_id=school_user.id
            )

            dm_create_student(school_id=str(school_user.id), class_id=str(cls.id), student_code=student['national_code'])
        
        return redirect('students')

    return render(request, 'form/add_students_from_excel.html')

def edit_student(request, national_code):
    current_user = request.user

    student = Student.objects.filter(Q(student_national_code=national_code)&Q(school_id=current_user.id)).first()
    if student is None:
        return redirect('unknown_student_info')
    
    if request.method == 'POST':
        student_name = request.POST.get("student_name")
        student_family = request.POST.get("student_family")
        student_national_code = request.POST.get("student_national_code")
        student_password = request.POST.get("student_password")
        student_phone_number = request.POST.get("student_phone_number")

        if Student.objects.filter(Q(student_national_code=student_national_code) & Q(student_phone_number=student_phone_number)):
            return redirect('duplicated_student_info')

        student.name = student_name
        student.student_family = student_family
        student.student_national_code = student_national_code
        student.student_password = student_password
        student.student_phone_number = student_phone_number

        student.save()

        dm_edit_student(school_id=str(current_user.id), class_id=str(student.student_class.id), old_student_code=national_code, new_student_code=student_national_code)
        
        return redirect('students')
    
    return render(request, 'form/edit_student.html', {'student': student})

def remove_student(request, national_code):
    current_user = request.user

    student = Student.objects.filter(Q(student_national_code=national_code)&Q(school_id=current_user.id)).first()
    if student is None:
        return redirect('unknown_student_info')
    
    Student.delete(student)

    dm_delete_student(school_id=str(current_user.id), class_id=str(student.student_class.id), student_code=student.student_national_code)
        
    return redirect('students')

def student_info(request, national_code):
    current_user = request.user

    student = Student.objects.filter(Q(student_national_code=national_code)&Q(school_id=current_user.id)).first()
    if student is None:
        return redirect('unknown_student_info')

    return redirect('content/student_info', {'data':student})
    