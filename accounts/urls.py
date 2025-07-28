from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.school_login_view, name='login'),
    path('signup/', views.school_signup_view, name='signup'),

    path('error/duplicate-school/', views.duplicate_school_error_view, name='error_duplicate_school'),
    path('error/unknown-school/', views.unknown_school_error_view, name='error_unknown_school'),
    path('success/registration/', views.registration_success_view, name='success_registration'),
]
