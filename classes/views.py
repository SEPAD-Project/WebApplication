import json
import os

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Class
from utils.base_path_finder import find_base_path
from utils.excel_reading import add_classes
from utils.generate_class_code import generate_class_code
from utils.server.Website.directory_manager import dm_create_class, dm_delete_class


# View to list all classes for the current logged-in user (school)
@login_required
def classes(request):
    current_user = request.user
    class_list = current_user.classes.all()
    return render(request, 'main/classes.html', {'classes': class_list})


# View to manually add a single class
@login_required
def add_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        current_user = request.user
        school_code = current_user.school_code

        class_code = generate_class_code(school_code, class_name)

        if Class.objects.filter(class_code=class_code).exists():
            return redirect('duplicated_class_info')

        new_class = Class.objects.create(
            class_name=class_name,
            class_code=class_code,
            school=current_user
        )

        # Create directory for new class
        dm_create_class(
            school_id=str(current_user.id),
            class_id=str(new_class.id)
        )

        return redirect('classes')

    return render(request, 'form/add_class.html')


# View to import classes from an uploaded Excel file
@login_required
def add_classes_from_excel(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file_input']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)

        sheet_name = request.POST.get('sheet')
        name_letter = request.POST.get('name')

        existing_classes = [cls.class_name for cls in Class.objects.all()]
        school_user = request.user

        result = add_classes(
            filename, sheet_name, name_letter,
            existing_classes, school_user.school_code
        )

        if result in ['sheet_not_found', 'bad_column_letter']:
            excel_errors = [result]
            response = HttpResponseRedirect(reverse('error_in_class_excel'))
            response.set_cookie('excel_errors', json.dumps(excel_errors), max_age=3600)
            return response

        if isinstance(result[0], list):
            excel_errors = []
            for problem in result:
                cell = f"{problem[2]}{problem[1]}"
                if problem[0] == "bad_format":
                    excel_errors.append(f"Bad data format in cell {cell}.")
                elif problem[0] == "duplicated_name":
                    excel_errors.append(f"Duplicated value in cell {cell}.")
                else:
                    excel_errors.append(f"Unknown issue in cell {cell}.")

            response = HttpResponseRedirect(reverse('error_in_class_excel'))
            response.set_cookie('excel_errors', json.dumps(excel_errors), max_age=3600)
            return response

        for cls in result:
            Class.objects.create(
                class_name=cls['name'],
                class_code=cls['code'],
                school_id=school_user.id,
            )

        return redirect('classes')

    return render(request, 'form/add_classes_from_excel.html')


# View to display details of a specific class
@login_required
def class_info(request, class_name):
    current_user = request.user
    data = Class.objects.filter(
        Q(class_name=class_name) & Q(school=current_user.id)
    ).first()

    if data is None:
        return redirect('unknown_class_info')

    return render(
        request,
        'content/class_info.html',
        {
            'data': data,
            'teachers': data.teachers.all(),
            'students': data.students.all()
        }
    )


# View to edit a class’s name or upload new schedule file
@login_required
def edit_class(request, class_name):
    current_user = request.user
    data = Class.objects.filter(
        Q(class_name=class_name) & Q(school=current_user.id)
    ).first()

    if data is None:
        return redirect('unknown_class_info')

    if request.method == 'POST':
        new_name = request.POST.get("class_name")
        uploaded_file = request.FILES.get('file-input')

        if new_name != class_name:
            if Class.objects.filter(Q(class_name=new_name) & Q(school=current_user.id)).exists():
                return redirect('duplicated_class_info')

            new_code = generate_class_code(current_user.school_code, new_name)
            data.class_name = new_name
            data.class_code = new_code
            data.save()

        if uploaded_file:
            save_path = os.path.join(find_base_path(), str(current_user.id), str(data.id))
            file_path = os.path.join(save_path, "schedule.xlsx")

            with open(file_path, 'wb+') as dest:
                for chunk in uploaded_file.chunks():
                    dest.write(chunk)

        return redirect('classes')

    return render(request, 'form/edit_class.html', {'name': data.class_name})


# View to delete a class
@login_required
def remove_class(request, class_name):
    current_user = request.user
    cls = Class.objects.filter(
        Q(class_name=class_name) & Q(school=current_user.id)
    ).first()

    if cls is None:
        return redirect('unknown_student_info')

    dm_delete_class(school_id=str(current_user.id), class_id=str(cls.id))
    cls.delete()

    return redirect('classes')


# View to handle duplicated class error
def duplicated_class_info(request):
    return render(request, 'error/duplicated_class_info.html')


# View to handle Excel-related import errors
def error_in_class_excel(request):
    errors = json.loads(request.COOKIES.get('excel_errors', '[]'))
    return render(request, 'error/error_in_class_excel.html', {'texts': errors})


# View for class file permission error
def class_file_permission_error(request):
    return render(request, 'error/class_file_permission_error.html')


# View for unknown class name error
def unknown_class_info(request):
    return render(request, 'error/unknown_class_info.html')


# View for general schedule error
def error_in_schedule(request):
    return render(request, 'error/error_in_schedule.html')
