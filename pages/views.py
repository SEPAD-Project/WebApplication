from django.shortcuts import render


# Home page
def home_page_view(request):
    return render(request, 'main/home.html')


# About page
def about_page_view(request):
    return render(request, 'content/about.html')


# Downloads page
def downloads_page_view(request):
    return render(request, 'content/downloads.html')


# Contact page
def contact_page_view(request):
    return render(request, 'content/contact.html')


# Coming soon page
def coming_soon_page_view(request):
    return render(request, 'content/coming_soon.html')


# 404 error page
def error_404_view(request):
    return render(request, 'error/404.html')


# 429 error page (Too Many Requests)
def error_429_view(request):
    return render(request, 'error/429.html')
