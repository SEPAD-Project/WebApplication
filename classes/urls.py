from django.urls import path
from . import views

app_name = 'classes'

urlpatterns = [
    path('', views.class_list_view, name='list'),
    path('add/', views.class_create_view, name='create'),
    path('import/', views.class_bulk_upload_view, name='import'),
    path('<str:class_name>/', views.class_detail_view, name='detail'),
    path('<str:class_name>/edit/', views.class_edit_view, name='edit'),
    path('<str:class_name>/delete/', views.class_delete_view, name='delete'),

    # Error pages
    path('error/duplicate/', views.duplicate_class_error_view, name='error_duplicate'),
    path('error/excel/', views.class_excel_error_view, name='error_excel'),
    path('error/permission/', views.class_file_permission_error_view, name='error_permission'),
    path('error/not-found/', views.unknown_class_error_view, name='error_not_found'),
    path('error/schedule/', views.schedule_error_view, name='error_schedule'),
]
