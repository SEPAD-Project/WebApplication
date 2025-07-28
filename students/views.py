import json
import os
import zipfile

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Student
from classes.models import Class
from utils.excel_reading import add_students
from utils.server.Website.directory_manager import (
    dm_create_student, dm_edit_student, dm_delete_student
)
from utils.base_path_finder import find_base_path


# View to list all students in current school
def students(request):
    current_user = request.user
    student_list = current_user.students.all()
    return render(request, 'main/students.html', {'students': student_list})


# View to manually add a new student
def add_student(request):
    current_user = request.user

    if request.method == 'POST':
        name = request.POST.get('student_name')
        family = request.POST.get('student_family')
        national_code = request.POST.get('student_national_code')
        password = request.POST.get('student_password')
        phone = request.POST.get('student_phone_number')
        uploaded_file = request.FILES['file_input']
        selected_class_id = request.POST.get('selected_class')

        if Student.objects.filter(
            Q(student_national_code=national_code) | Q(student_phone_number=phone)
        ).exists():
            return redirect('duplicated_student_info')

        student_class = Class.objects.get(id=int(selected_class_id))

        student = Student.objects.create(
            student_name=name,
            student_family=family,
            student_national_code=national_code,
            student_password=password,
            student_phone_number=phone,
            student_class=student_class,
            school=current_user
        )

        save_path = os.path.join(find_base_path(), str(current_user.id), str(student_class.id))
        file_path = os.path.join(save_path, f"{national_code}.jpg")

        with open(file_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        dm_create_student(
            school_id=str(current_user.id),
            class_id=str(student_class.id),
            student_code=national_code
        )

        return redirect('students')

    return render(request, 'form/add_student.html', {'classes': current_user.classes.all()})


# View to add students from Excel and ZIP files
@login_required
def add_students_from_excel(request):
    if request.method == 'POST':
        current_user = request.user
        uploaded_excel = request.FILES['file_input']
        zip_file = request.FILES.get('zip_input')
        fs = FileSystemStorage()
        filename = fs.save(uploaded_excel.name, uploaded_excel)

        sheet_name = request.POST.get('sheet')
        name_letter = request.POST.get('name')
        family_letter = request.POST.get('family')
        nc_letter = request.POST.get('national_code')
        class_letter = request.POST.get('class')
        pass_letter = request.POST.get('password')
        phone_letter = request.POST.get('phone_number')

        classes = Class.objects.all()
        students = Student.objects.all()

        result = add_students(
            filename, sheet_name, name_letter, family_letter, nc_letter,
            class_letter, pass_letter, phone_letter,
            [cls.class_name for cls in classes],
            [s.student_national_code for s in students],
            [s.student_phone_number for s in students],
            current_user.school_code
        )

        if result in ['sheet_not_found', 'bad_column_letter']:
            response = HttpResponseRedirect(reverse('error_in_student_excel'))
            response.set_cookie('excel_errors', json.dumps([result]), max_age=3600)
            return response

        if isinstance(result[0], list):
            excel_errors = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    excel_errors.append(f"Bad data format in cell {cell}.")
                elif problem[0] == "duplicated_nc":
                    excel_errors.append(f"Duplicated national code in cell {cell}.")
                elif problem[0] == "unknown_class":
                    excel_errors.append(f"Unknown class name in cell {cell}.")
                else:
                    excel_errors.append(f"Unknown issue in cell {cell}.")

            response = HttpResponseRedirect(reverse('error_in_student_excel'))
            response.set_cookie('excel_errors', json.dumps(excel_errors), max_age=3600)
            return response

        zip_errors = []
        for student in result:
            cls = Class.objects.filter(class_code=student['class']).first()
            expected_path = f"{zip_file.name[:-4]}/{cls.class_name}/{student['national_code']}.jpg"
            with zipfile.ZipFile(zip_file) as zf:
                if expected_path not in zf.namelist():
                    zip_errors.append(expected_path)

        if zip_errors:
            response = HttpResponseRedirect(reverse('error_in_student_zip'))
            response.set_cookie('zip_errors', json.dumps(zip_errors), max_age=3600)
            return response

        for student in result:
            cls = Class.objects.filter(class_code=student['class']).first()
            new_student = Student.objects.create(
                student_name=student['name'],
                student_family=student['family'],
                student_national_code=student['national_code'],
                student_phone_number=student['phone_number'],
                student_class=cls,
                student_password=student['password'],
                school_id=current_user.id
            )

            save_path = os.path.join(find_base_path(), str(current_user.id), str(cls.id))
            file_path = os.path.join(save_path, f"{student['national_code']}.jpg")
            zip_inner_path = f"{zip_file.name[:-4]}/{cls.class_name}/{student['national_code']}.jpg"

            with zipfile.ZipFile(zip_file) as zf:
                if zip_inner_path in zf.namelist():
                    with zf.open(zip_inner_path) as photo:
                        with open(file_path, 'wb') as dest:
                            dest.write(photo.read())

            dm_create_student(
                school_id=str(current_user.id),
                class_id=str(cls.id),
                student_code=student['national_code']
            )

        return redirect('students')

    return render(request, 'form/add_students_from_excel.html')


# View to edit student info
def edit_student(request, national_code):
    current_user = request.user
    student = Student.objects.filter(
        Q(student_national_code=national_code) & Q(school_id=current_user.id)
    ).first()

    if student is None:
        return redirect('unknown_student_info')

    if request.method == 'POST':
        name = request.POST.get("student_name")
        family = request.POST.get("student_family")
        new_nc = request.POST.get("student_national_code")
        password = request.POST.get("student_password")
        phone = request.POST.get("student_phone_number")

        if Student.objects.filter(
            Q(student_national_code=new_nc) & Q(student_phone_number=phone)
        ).exclude(id=student.id).exists():
            return redirect('duplicated_student_info')

        student.student_name = name
        student.student_family = family
        student.student_national_code = new_nc
        student.student_password = password
        student.student_phone_number = phone
        student.save()

        dm_edit_student(
            school_id=str(current_user.id),
            class_id=str(student.student_class.id),
            old_student_code=national_code,
            new_student_code=new_nc
        )

        return redirect('students')

    return render(request, 'form/edit_student.html', {'student': student})


# View to delete a student
def remove_student(request, national_code):
    current_user = request.user
    student = Student.objects.filter(
        Q(student_national_code=national_code) & Q(school_id=current_user.id)
    ).first()

    if student is None:
        return redirect('unknown_student_info')

    dm_delete_student(
        school_id=str(current_user.id),
        class_id=str(student.student_class.id),
        student_code=student.student_national_code
    )

    student.delete()

    return redirect('students')


# View to show student profile
def student_info(request, national_code):
    current_user = request.user
    student = Student.objects.filter(
        Q(student_national_code=national_code) & Q(school_id=current_user.id)
    ).first()

    if student is None:
        return redirect('unknown_student_info')

    return render(request, 'content/student_info.html', {'data': student})


# Error page views
def duplicated_student_info(request):
    return render(request, 'error/duplicated_student_info.html')


def error_in_student_excel(request):
    errors = json.loads(request.COOKIES.get('excel_errors', '[]'))
    return render(request, 'error/error_in_student_excel.html', {'texts': errors})


def error_in_student_zip(request):
    errors = json.loads(request.COOKIES.get('zip_errors', '[]'))
    return render(request, 'error/error_in_student_zip.html', {'texts': errors})


def student_file_permission_error(request):
    return render(request, 'error/student_file_permission_error.html')


def unknown_student_info(request):
    return render(request, 'error/unknown_student_info.html')
