from django.urls import path
from . import views

urlpatterns = [
    path('', views.students, name='students'),
    path('/add_student', views.add_student, name='add_student'),
    path('/student_file_permission_error', views.student_file_permission_error, name='student_file_permission_error'),
    path('/duplicated_student_info', views.duplicated_student_info, name='duplicated_student_info'),
    path('/error_in_student_excel', views.error_in_student_excel, name='error_in_student_excel'),
    path('/unknown_student_info', views.unknown_student_info, name='unknown_student_info'),
    path('/add_students_from_excel', views.add_students_from_excel, name='add_students_from_excel'),
    path('/edit_student/<str:national_code>', views.edit_student, name='edit_student'),
    path('/remove_student/<str:national_code>', views.remove_student, name='remove_student'),
    path('/student_info/<str:national_code>', views.student_info, name='student_info'),
]
