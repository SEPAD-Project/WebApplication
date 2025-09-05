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
]
