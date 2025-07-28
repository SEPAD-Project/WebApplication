from django.urls import path, include

urlpatterns = [
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),

    path('panel/', include('schools.urls')),
    path('panel/classes/', include('classes.urls')),
    path('panel/students/', include('students.urls')),
    path('panel/teachers/', include('teachers.urls')),
    path('panel/analytics/', include('analytics.urls')),
]
