from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('school-info/', views.school_overview_view, name='school_overview'),
]
