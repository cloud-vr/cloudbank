from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world. You're at the bank index.")

def login_page(request):
    return render(request, 'bank/login.html')

def login_button(request):
    return HttpResponse("You clicked the login button.")