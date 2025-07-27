from django.urls import path
from . import views

urlpatterns = [
    path('/login', views.login_view, name='login'),
    path('/signup', views.signup, name='signup'),
    path('/duplicated_school_info', views.duplicated_school_info, name='duplicated_school_info'),
    path('/notify_username_password', views.notify_username_password, name='notify_username_password'),
    path('/unknown_school_info', views.unknown_school_info, name='unknown_school_info'),
]