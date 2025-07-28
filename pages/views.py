from django.shortcuts import render


# Home page
def home(request):
    return render(request, 'main/home.html')


# About page
def about(request):
    return render(request, 'content/about.html')


# Downloads page
def downloads(request):
    return render(request, 'content/downloads.html')


# Contact page
def contact(request):
    return render(request, 'content/contact.html')


# Coming soon page
def comings_soon(request):
    return render(request, 'content/coming_soon.html')


# 404 error page
def page_404(request):
    return render(request, 'error/404.html')


# 429 error page (Too Many Requests)
def page_429(request):
    return render(request, 'error/429.html')
