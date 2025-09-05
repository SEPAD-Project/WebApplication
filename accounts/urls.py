from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.school_login_view, name='login'),
    path('signup/', views.school_signup_view, name='signup'),
]
