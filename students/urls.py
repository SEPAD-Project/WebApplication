from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.student_list_view, name='list'),
    path('add/', views.student_create_view, name='create'),
    path('import/', views.student_bulk_upload_view, name='import'),
    path('<str:national_code>/', views.student_detail_view, name='detail'),
    path('<str:national_code>/edit/', views.student_edit_view, name='edit'),
    path('<str:national_code>/delete/', views.student_delete_view, name='delete'),

    # Errors
    path('error/duplicate/', views.duplicate_student_error_view, name='error_duplicate'),
    path('error/excel/', views.student_excel_error_view, name='error_excel'),
    path('error/zip/', views.student_zip_error_view, name='error_zip'),
    path('error/permission/', views.student_file_permission_error_view, name='error_permission'),
    path('error/not-found/', views.unknown_student_error_view, name='error_not_found'),
]
