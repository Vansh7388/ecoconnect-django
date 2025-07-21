from django.shortcuts import render
from django.http import HttpResponse

def event_list(request):
    return render(request, 'events/event_list.html')

def create_event(request):
    return HttpResponse("<h1>Create Event</h1><p>Coming Soon...</p>")