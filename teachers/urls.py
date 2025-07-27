from django.urls import path
from . import views

urlpatterns = [
    path('', views.teachers, name='teachers'),
    path('/add_teacher', views.add_teacher, name='add_teacher'),
    path('/teacher_info/<str:national_code>', views.teacher_info, name='teacher_info'),
    path('/wrong_teacher_info', views.wrong_teacher_info, name='wrong_teacher_info'),
    path('/edit_teacher/<str:national_code>', views.edit_teacher, name='edit_teacher'),
    path('/remove_teacher/<str:national_code>', views.remove_teacher, name='remove_teacher'),
]