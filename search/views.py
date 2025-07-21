from django.shortcuts import render
from django.http import HttpResponse
from events.models import Event
from django.utils import timezone

def home(request):
    # Get upcoming events (limit to 3 for homepage)
    featured_events = Event.objects.filter(
        date_time__gte=timezone.now(),
        status='upcoming'
    ).order_by('date_time')[:3]
    
    # Get some statistics
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(status='upcoming').count()
    
    context = {
        'featured_events': featured_events,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
    }
    
    return render(request, 'search/home.html', context)