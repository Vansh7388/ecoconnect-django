from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from events.models import Event
from .models import EventParticipation, PhotoUpload, UserHistory
from .forms import PhotoUploadForm
from django.db.models import Count, Q

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
    
    # Add recent photo uploads
    for photo in PhotoUpload.objects.filter(user=user).order_by('-upload_date')[:3]:
        recent_activity.append({
            'description': f'You uploaded a photo for "{photo.event.title}"',
            'date': photo.upload_date
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

@login_required
def upload_photo(request, event_id=None):
    # Get events the user can upload photos for (organized events or events they participated in)
    user_events = Event.objects.filter(
        Q(organizer=request.user) | Q(eventparticipation__user=request.user)
    ).distinct().order_by('-date_time')
    
    selected_event = None
    if event_id:
        selected_event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event_id = request.POST.get('event')
        if not event_id:
            messages.error(request, 'Please select an event.')
            return render(request, 'interaction/upload_photo.html', {
                'user_events': user_events,
                'selected_event': selected_event
            })
        
        event = get_object_or_404(Event, id=event_id)
        
        # Check if user has permission to upload for this event
        if not (event.organizer == request.user or 
                EventParticipation.objects.filter(user=request.user, event=event).exists()):
            messages.error(request, 'You can only upload photos for events you organized or attended.')
            return render(request, 'interaction/upload_photo.html', {
                'user_events': user_events,
                'selected_event': selected_event
            })
        
        # Handle file upload
        if 'image' not in request.FILES:
            messages.error(request, 'Please select an image to upload.')
            return render(request, 'interaction/upload_photo.html', {
                'user_events': user_events,
                'selected_event': selected_event
            })
        
        # Create photo upload
        photo = PhotoUpload.objects.create(
            event=event,
            user=request.user,
            image=request.FILES['image'],
            caption=request.POST.get('caption', '')
        )
        
        messages.success(request, f'Photo uploaded successfully for "{event.title}"!')
        return redirect('interaction:dashboard')
    
    context = {
        'user_events': user_events,
        'selected_event': selected_event,
    }
    
    return render(request, 'interaction/upload_photo.html', context)