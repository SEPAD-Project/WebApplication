from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Teacher
from classes.models import Class

from utils.generate_class_code import reverse_class_code

def teachers(request):
    currect_user = request.user
    teachers = currect_user.teachers.all()
    return render(request, 'teachers.html', {'teachers':teachers})

def add_teacher(request):
    current_user = request.user
    if request.method == 'POST':
        national_code = request.POST.get('teacher_national_code')
        password = request.POST.get('teacher_password')

        teacher = Teacher.objects.filter(Q(teacher_national_code=national_code)  & Q(teacher_password=password)).first()
        if teacher is None:
            return redirect('wrong_teacher_info')
        
        classes = request.POST.getlist('selected_classes')
        for class_id in classes:
            cls = Class.objects.filter(id=int(class_id)).first()
            cls.teachers.add(teacher)

        current_user.teachers.add(teacher)
        
        return redirect('teachers')
    
    school_classes = current_user.classes.all()
    return render(request, 'add_teacher.html', {'classes':school_classes})

def teacher_info(request, national_code):
    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')
    
    current_user = request.user
    school_teachers = current_user.teachers.all()

    if not (teacher in school_teachers):
        return redirect('wrong_teacher_info')

    return render(request, 'teacher_info.html', {'data':teacher})

def wrong_teacher_info(request):
    return render(request, 'wrong_teacher_info.html')

def edit_teacher(request, national_code):
    current_user = request.user
    if request.method == 'POST':
        new_classes = request.POST.getlist('selected_classes')
        if new_classes == []:
            return redirect('teachers')

        teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
        if teacher is None:
            return redirect('wrong_teacher_info')
        
        teacher_classes = teacher.classes.all()
        for cls in teacher_classes:
            class_code = cls.class_code
            class_school_code = reverse_class_code(class_code)[0]
            if class_school_code == current_user.school_code:
                teacher.classes.remove(cls)
        
        for cls_code in new_classes:
            cls = Class.objects.filter(class_code=cls_code).first()
            teacher.classes.add(cls)
        
        return redirect('teachers')


    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')

    school_teachers = current_user.teachers.all()
    school_classes = current_user.classes.all()

    if not (teacher in school_teachers):
        return redirect('wrong_teacher_info')
    
    return render(request, 'edit_teacher.html', {'teacher':teacher, 'classes':school_classes})

def remove_teacher(request, national_code):
    teacher = Teacher.objects.filter(teacher_national_code=national_code).first()
    if teacher is None:
        return redirect('wrong_teacher_info')
    
    current_user = request.user
    school_teachers = current_user.teachers.all()

    if not (teacher in school_teachers):
        return redirect('wrong_teacher_info')
    
    teacher_classes = teacher.classes.all()
    for cls in teacher_classes:
        class_code = cls.class_code
        class_school_code = reverse_class_code(class_code)[0]
        if class_school_code == current_user.school_code:
            teacher.classes.remove(cls)

    current_user.teachers.remove(teacher)

    return redirect(request, 'teachers.html')
