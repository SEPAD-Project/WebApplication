from django.urls import path
from . import views

urlpatterns = [
    path('/home', views.panel_entry, name='panel_entry'),
    path('/school_info', views.school_info, name='school_info'),
]