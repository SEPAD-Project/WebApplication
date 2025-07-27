from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def downloads(request):
    return render(request, 'downloads.html')

def contact(request):
    return render(request, 'contact.html')

def comings_soon(request):
    return render(request, 'coming_soon.html')

def page_404(request):
    return render(request, '404.html')

def page_429(request):
    return render(request, '429.html')