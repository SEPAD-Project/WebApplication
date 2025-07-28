from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_dashboard_view, name='dashboard'),

    path('class-students/', views.class_accuracy_report_view, name='class_accuracy'),
    
    path('student-lesson/', views.student_lesson_accuracy_report_view, name='student_lesson_accuracy'),
    path('student-week/', views.student_week_accuracy_report_view, name='student_week_accuracy'),

    path('school-teachers-performance/', views.school_teachers_performance_report_view, name='school_teachers_performance'),
    path('school-classes-accuracy/', views.school_classes_accuracy_report_view, name='school_classes_accuracy'),
]
