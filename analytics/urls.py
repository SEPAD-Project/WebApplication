from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_menu, name='analytics_menu'),
    path('/select_student_for_lesson_accuracy', views.select_student_for_lesson_accuracy, name='select_student_for_lesson_accuracy'),
    path('/select_student_for_week_accuracy', views.select_student_for_week_accuracy, name='select_student_for_week_accuracy'),
    path('/select_class_for_students_accuracy', views.select_class_for_students_accuracy, name='select_class_for_students_accuracy'),
    path('/school_teachers_performance', views.school_teachers_performance, name='school_teachers_performance'),
    path('/school_classes_accuracy', views.school_classes_accuracy, name='school_classes_accuracy'),
]