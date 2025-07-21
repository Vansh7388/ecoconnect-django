from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("<h1>User Dashboard</h1><p>Coming Soon...</p>")

def upload_photo(request):
    return HttpResponse("<h1>Upload Photo</h1><p>Coming Soon...</p>")