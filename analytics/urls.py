from django.urls import path
from . import views

urlpatterns = [
    path('', views.analytics_menu, name='analytics_menu'),
]