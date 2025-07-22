from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from events.models import Event
from .models import EventParticipation, PhotoUpload, UserHistory
from .forms import PhotoUploadForm
from django.db.models import Count, Q, Prefetch

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
    
    # Get user's organized events with photo counts (limit to recent 5)
    organized_events = Event.objects.filter(
        organizer=user
    ).prefetch_related(
        'photos'
    ).annotate(
        photo_count=Count('photos')
    ).order_by('-date_time')[:5]
    
    # Get events user is participating in with photo counts (limit to recent 5)
    joined_events = EventParticipation.objects.filter(
        user=user
    ).select_related(
        'event__organizer', 
        'event__category', 
        'event__location'
    ).prefetch_related(
        'event__photos'
    ).annotate(
        event_photo_count=Count('event__photos')
    ).order_by('-joined_date')[:5]
    
    # Create enhanced recent activity timeline
    recent_activity = []
    
    # Add recent events organized with more detail
    for event in Event.objects.filter(organizer=user).order_by('-created_at')[:3]:
        status_text = "organized"
        if event.status == 'completed':
            status_text = "completed"
        elif event.status == 'ongoing':
            status_text = "started"
        
        recent_activity.append({
            'description': f'You {status_text} "{event.title}" - {event.category.name}',
            'date': event.created_at,
            'type': 'organized',
            'event_id': event.id
        })
    
    # Add recent participations with more detail
    for participation in EventParticipation.objects.filter(user=user).select_related('event').order_by('-joined_date')[:3]:
        event_status = ""
        if participation.event.status == 'completed':
            event_status = " (completed)"
        
        recent_activity.append({
            'description': f'You joined "{participation.event.title}"{event_status}',
            'date': participation.joined_date,
            'type': 'joined',
            'event_id': participation.event.id
        })
    
    # Add recent photo uploads with event context
    for photo in PhotoUpload.objects.filter(user=user).select_related('event').order_by('-upload_date')[:3]:
        recent_activity.append({
            'description': f'You shared a photo from "{photo.event.title}"',
            'date': photo.upload_date,
            'type': 'photo',
            'event_id': photo.event.id
        })
    
    # Sort activity by date and limit to 5 most recent
    recent_activity.sort(key=lambda x: x['date'], reverse=True)
    recent_activity = recent_activity[:5]
    
    # Get memory events (completed events with photos)
    memory_events = Event.objects.filter(
        Q(organizer=user) | Q(eventparticipation__user=user),
        status='completed'
    ).annotate(
        photo_count=Count('photos')
    ).filter(photo_count__gt=0).distinct()[:3]
    
    context = {
        'events_organized': events_organized,
        'events_joined': events_joined,
        'photos_uploaded': photos_uploaded,
        'total_visits': total_visits,
        'organized_events': organized_events,
        'joined_events': joined_events,
        'recent_activity': recent_activity,
        'memory_events': memory_events,
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
        
        # Handle file upload with form validation
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create photo upload
                photo = form.save(commit=False)
                photo.event = event
                photo.user = request.user
                photo.save()
                
                # Create activity entry
                activity_desc = f'You added a photo to "{event.title}"'
                if event.status == 'completed':
                    activity_desc = f'You added a memory to "{event.title}"'
                
                messages.success(request, f'Photo uploaded successfully for "{event.title}"!')
                return redirect('interaction:dashboard')
                
            except Exception as e:
                messages.error(request, f'Error uploading photo: {str(e)}')
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_name = form.fields[field].label or field.title()
                        messages.error(request, f'{field_name}: {error}')
    
    context = {
        'user_events': user_events,
        'selected_event': selected_event,
    }
    
    return render(request, 'interaction/upload_photo.html', context)