from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('about/', views.about_page_view, name='about'),
    path('downloads/', views.downloads_page_view, name='downloads'),
    path('contact/', views.contact_page_view, name='contact'),
    path('coming-soon/', views.coming_soon_page_view, name='coming_soon'),

    # Errors
    path('error/404/', views.error_404_view, name='error_404'),
    path('error/429/', views.error_429_view, name='error_429'),
]
