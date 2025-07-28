from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list_view, name='list'),
    path('add/', views.teacher_add_view, name='add'),
    path('<str:national_code>/', views.teacher_detail_view, name='detail'),
    path('<str:national_code>/update/', views.teacher_update_view, name='update'),
    path('<str:national_code>/remove/', views.teacher_remove_view, name='remove'),

    # Errors
    path('error/not-found/', views.invalid_teacher_error_view, name='error_invalid'),
]
