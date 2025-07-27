from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_menu, name='analytics_menu'),
    path('/compare_student_accuracy_lesson', views.compare_student_accuracy_lesson, name='compare_student_accuracy_lesson'),
    path('/compare_student_accuracy_week', views.compare_student_accuracy_week, name='compare_student_accuracy_week'),
    path('/compare_students', views.compare_students, name='compare_students'),
]