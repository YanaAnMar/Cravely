from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, '../templates/homepage.html')

def profile(request):
    return render(request, '../templates/profile.html')

def recipepage(request):
    return render(request, '../templates/recipepage.html')
