from django.db.models import Q
from django.shortcuts import redirect, render

from .models import Teacher
from classes.models import Class
from utils.generate_class_code import reverse_class_code


# View to list all teachers for the current school user
def teachers(request):
    current_user = request.user
    teacher_list = current_user.teachers.all()
    return render(request, 'main/teachers.html', {'teachers': teacher_list})


# View to add an existing teacher to the school and assign classes
def add_teacher(request):
    current_user = request.user

    if request.method == 'POST':
        national_code = request.POST.get('teacher_national_code')
        password = request.POST.get('teacher_password')

        teacher = Teacher.objects.filter(
            Q(teacher_national_code=national_code) & Q(teacher_password=password)
        ).first()

        if teacher is None:
            return redirect('wrong_teacher_info')

        class_ids = request.POST.getlist('selected_classes')
        for class_id in class_ids:
            cls = Class.objects.filter(id=int(class_id)).first()
            if cls:
                cls.teachers.add(teacher)

        current_user.teachers.add(teacher)

        return redirect('teachers')

    school_classes = current_user.classes.all()
    return render(request, 'form/add_teacher.html', {'classes': school_classes})


# View to display teacher information if they belong to current school
def teacher_info(request, national_code):
    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')

    current_user = request.user
    if teacher not in current_user.teachers.all():
        return redirect('wrong_teacher_info')

    return render(request, 'content/teacher_info.html', {'data': teacher})


# View to render error page when teacher info is invalid
def wrong_teacher_info(request):
    return render(request, 'error/wrong_teacher_info.html')


# View to edit teacher’s assigned classes
def edit_teacher(request, national_code):
    current_user = request.user

    if request.method == 'POST':
        new_classes = request.POST.getlist('selected_classes')
        if not new_classes:
            return redirect('teachers')

        teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
        if teacher is None:
            return redirect('wrong_teacher_info')

        # Remove teacher from existing classes in current school
        for cls in teacher.classes.all():
            class_code = cls.class_code
            class_school_code = reverse_class_code(class_code)[0]
            if class_school_code == current_user.school_code:
                teacher.classes.remove(cls)

        # Assign teacher to new selected classes
        for class_code in new_classes:
            cls = Class.objects.filter(class_code=class_code).first()
            if cls:
                teacher.classes.add(cls)

        return redirect('teachers')

    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')

    if teacher not in current_user.teachers.all():
        return redirect('wrong_teacher_info')

    school_classes = current_user.classes.all()

    return render(request, 'form/edit_teacher.html', {
        'teacher': teacher,
        'classes': school_classes
    })


# View to remove a teacher from the current school and detach their classes
def remove_teacher(request, national_code):
    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')

    current_user = request.user

    if teacher not in current_user.teachers.all():
        return redirect('wrong_teacher_info')

    # Remove teacher from classes belonging to this school
    for cls in teacher.classes.all():
        class_code = cls.class_code
        class_school_code = reverse_class_code(class_code)[0]
        if class_school_code == current_user.school_code:
            teacher.classes.remove(cls)

    current_user.teachers.remove(teacher)

    return redirect('teachers')
