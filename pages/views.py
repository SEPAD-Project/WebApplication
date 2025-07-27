from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def about(request):
    return render(request, 'content/about.html')

def downloads(request):
    return render(request, 'content/downloads.html')

def contact(request):
    return render(request, 'content/contact.html')

def comings_soon(request):
    return render(request, 'content/coming_soon.html')

def page_404(request):
    return render(request, 'error/404.html')

def page_429(request):
    return render(request, 'error/429.html')