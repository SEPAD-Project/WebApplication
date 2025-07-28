from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from students.models import Student
from .tasks import (
    task_generate_class_students_accuracy,
    task_generate_student_accuracy_by_lesson,
    task_generate_student_accuracy_by_week,
    task_generate_school_teachers_performance,
    task_generate_school_classes_accuracy,
)


# View to show main analytics menu
@login_required
def analytics_dashboard_view(request):
    return render(request, 'main/analytics_menu.html')


# View to select a class and trigger student accuracy report generation
@login_required
def class_accuracy_report_view(request):
    current_user = request.user

    if request.method == "POST":
        class_id = request.POST.get('selected_class')

        task_generate_class_students_accuracy(
            school_id=current_user.id,
            class_id=class_id,
            school_email=current_user.email
        )

    return render(
        request,
        'form/select_class_for_students_accuracy.html',
        {'classes': current_user.classes.all()}
    )


# View to select a student and generate accuracy-by-lesson report
@login_required
def student_lesson_accuracy_report_view(request):
    if request.method == "POST":
        current_user = request.user
        student_nc = request.POST.get('student_national_code')

        student = Student.objects.filter(student_national_code=student_nc).first()
        if student:
            task_generate_student_accuracy_by_lesson(
                school_id=current_user.id,
                name=student.student_name,
                family=student.student_family,
                national_code=student_nc,
                class_id=student.student_class.id,
                school_email=current_user.email
            )

    return render(request, 'form/select_student_for_lesson_accuracy.html')


# View to select a student and generate accuracy-by-week report
@login_required
def student_week_accuracy_report_view(request):
    if request.method == "POST":
        current_user = request.user
        student_nc = request.POST.get('student_national_code')

        student = Student.objects.filter(student_national_code=student_nc).first()
        if student:
            task_generate_student_accuracy_by_week(
                school_id=current_user.id,
                name=student.student_name,
                family=student.student_family,
                national_code=student_nc,
                class_id=student.student_class.id,
                school_email=current_user.email
            )

    return render(request, 'form/select_student_for_week_accuracy.html')


# View to trigger school teachers performance report
@login_required
def school_teachers_performance_report_view(request):
    current_user = request.user

    task_generate_school_teachers_performance(
        school_id=current_user.id,
        school_email=current_user.email
    )

    return redirect('dashboard')


# View to trigger school classes accuracy report
@login_required
def school_classes_accuracy_report_view(request):
    current_user = request.user

    task_generate_school_classes_accuracy(
        school_id=current_user.id,
        school_email=current_user.email
    )

    return redirect('dashboard')
