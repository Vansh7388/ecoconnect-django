from django.shortcuts import render
from django.http import HttpResponse

def login_view(request):
    return HttpResponse("<h1>Login Page</h1><p>Coming Soon...</p>")

def register_view(request):
    return HttpResponse("<h1>Register Page</h1><p>Coming Soon...</p>")