from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('downloads/', views.downloads, name='downloads'),
    path('contact/', views.contact, name='contact'),
    path('comings_soon/', views.comings_soon, name='comings_soon'),
    path('page_404/', views.page_404, name='page_404'),
    path('page_429/', views.page_429, name='page_429'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('duplicated_school_info/', views.duplicated_school_info, name='duplicated_school_info'),
    path('notify_username_password/', views.notify_username_password, name='notify_username_password'),
    path('unknown_school_info/', views.unknown_school_info, name='unknown_school_info'),
    path('panel/', views.panel_entry, name='panel_entry'),
    path('panel/school_info', views.school_info, name='school_info'),
]
