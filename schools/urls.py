from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('school-info/', views.school_overview_view, name='school_overview'),
]
