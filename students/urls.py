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
]
