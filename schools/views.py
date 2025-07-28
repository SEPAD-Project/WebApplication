from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# View for displaying the main dashboard after login
@login_required
def dashboard_view(request):
    return render(request, 'schools/dashboard.html')


# View to display school-related statistics and current school info
@login_required
def school_overview_view(request):
    current_user = request.user

    class_count = len(current_user.classes.all())
    teacher_count = len(current_user.teachers.all())
    student_count = len(current_user.students.all())

    return render(
        request,
        'schools/school_overview.html',
        {
            'data': current_user,
            'cc': class_count,
            'tc': teacher_count,
            'sc': student_count
        }
    )
