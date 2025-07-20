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
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]
