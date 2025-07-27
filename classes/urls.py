from django.urls import path
from . import views

urlpatterns = [
    path('', views.classes, name='classes'),
    path('/add_class/', views.add_class, name='add_class'),
    path('/add_classes_from_excel/', views.add_classes_from_excel, name='add_classes_from_excel'),
    path('/class_file_permission_error/', views.class_file_permission_error, name='class_file_permission_error'),
    path('/duplicated_class_info/', views.duplicated_class_info, name='duplicated_class_info'),
    path('/error_in_class_excel/', views.error_in_class_excel, name='error_in_class_excel'),
    path('/unknown_class_info/', views.unknown_class_info, name='unknown_class_info'),
    path('/error_in_schedule/', views.error_in_schedule, name='error_in_schedule'),
    path('/class_info/<str:class_name>/', views.class_info, name='class_info'),
    path('/edit_class/<str:class_name>/', views.edit_class, name='edit_class'),
    path('/remove_class/<str:class_name>/', views.remove_class, name='remove_class'),
]