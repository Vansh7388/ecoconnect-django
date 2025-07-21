from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to EcoConnect!</h1><p>Local Environmental Action Hub</p>")