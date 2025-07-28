from django.shortcuts import render


# Home page
def home_page_view(request):
    return render(request, 'pages/home_page.html')


# About page
def about_page_view(request):
    return render(request, 'pages/about_page.html')


# Downloads page
def downloads_page_view(request):
    return render(request, 'pages/downloads_page.html')


# Contact page
def contact_page_view(request):
    return render(request, 'pages/contact_page.html')


# Coming soon page
def coming_soon_page_view(request):
    return render(request, 'pages/coming_soon_page.html')


# 404 error page
def error_404_view(request):
    return render(request, 'pages/error_404.html')


# 429 error page (Too Many Requests)
def error_429_view(request):
    return render(request, 'pages/error_429.html')
