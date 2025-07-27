from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from students.models import Student

from .tasks import *

@login_required
def analytics_menu(request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
    return render(request, 'main/analytics_menu.html')

@login_required
def select_class_for_students_accuracy(request):     
    current_user = request.user   
    if request.method == "POST":
        class_id = request.POST.get('selected_class') 

        task_generate_class_students_accuracy(school_id=current_user.id, class_id=class_id, school_email=current_user.email)

    return render(request, 'form/select_class_for_students_accuracy.html', {'classes':current_user.classes.all()})

@login_required
def select_student_for_lesson_accuracy(request):  
    if request.method == "POST":
        current_user = request.user   
        student_nc = request.POST.get('student_national_code')

        student = Student.objects.filter(student_national_code=student).first()

        task_generate_student_accuracy_by_lesson(school_id=current_user.id, name=student.student_name, family=student.student_family, national_code=student_nc, class_id=student.student_class.id, school_email=current_user.email) 

    return render(request, 'form/select_student_for_lesson_accuracy.html')

@login_required
def select_student_for_week_accuracy(request):      
    if request.method == "POST":
        current_user = request.user   
        student_nc = request.POST.get('student_national_code')

        student = Student.objects.filter(student_national_code=student).first()

        task_generate_student_accuracy_by_week(school_id=current_user.id, name=student.student_name, family=student.student_family, national_code=student_nc, class_id=student.student_class.id, school_email=current_user.email)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    return render(request, 'form/select_student_for_week_accuracy.html')

@login_required
def school_teachers_performance(request):      
    if request.method == "POST":
        current_user = request.user
        task_generate_school_teachers_performance(school_id=current_user.id, school_email=current_user.email)

        return redirect('analytics_menu')
    
@login_required
def school_classes_accuracy(request):      
    if request.method == "POST":
        current_user = request.user
        task_generate_school_classes_accuracy(school_id=current_user.id, school_email=current_user.email)

        return redirect('analytics_menu')