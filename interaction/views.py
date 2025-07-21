from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from events.models import Event
from .models import EventParticipation, PhotoUpload, UserHistory
from django.db.models import Count

@login_required
def dashboard(request):
    user = request.user
    
    # Track this page visit
    UserHistory.objects.create(
        user=user,
        page_visited='Dashboard',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Get user statistics
    events_organized = Event.objects.filter(organizer=user).count()
    events_joined = EventParticipation.objects.filter(user=user).count()
    photos_uploaded = PhotoUpload.objects.filter(user=user).count()
    total_visits = UserHistory.objects.filter(user=user).count()
    
    # Get user's organized events (limit to recent 5)
    organized_events = Event.objects.filter(organizer=user).order_by('-date_time')[:5]
    
    # Get events user is participating in (limit to recent 5)
    joined_events = EventParticipation.objects.filter(user=user).select_related('event').order_by('-joined_date')[:5]
    
    # Create recent activity timeline
    recent_activity = []
    
    # Add recent events organized
    for event in Event.objects.filter(organizer=user).order_by('-created_at')[:3]:
        recent_activity.append({
            'description': f'You organized "{event.title}"',
            'date': event.created_at
        })
    
    # Add recent participations
    for participation in EventParticipation.objects.filter(user=user).order_by('-joined_date')[:3]:
        recent_activity.append({
            'description': f'You joined "{participation.event.title}"',
            'date': participation.joined_date
        })
    
    # Sort activity by date
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    recent_activity = recent_activity[:5]  # Limit to 5 most recent
    
    context = {
        'events_organized': events_organized,
        'events_joined': events_joined,
        'photos_uploaded': photos_uploaded,
        'total_visits': total_visits,
        'organized_events': organized_events,
        'joined_events': joined_events,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'interaction/dashboard.html', context)

def upload_photo(request):
    return HttpResponse("<h1>Upload Photo</h1><p>Coming Soon...</p>")