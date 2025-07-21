from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from .forms import EventCreationForm, EventEditForm
from .models import Event, EventCategory
from django.db.models import Q

def event_list(request):
    events = Event.objects.all().order_by('date_time')
    
    # Handle search functionality
    search_query = request.GET.get('search')
    category_filter = request.GET.get('category')
    date_filter = request.GET.get('date')
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    if category_filter:
        events = events.filter(category__name__icontains=category_filter)
    
    if date_filter:
        events = events.filter(date_time__date=date_filter)
    
    # Get categories for the filter dropdown
    categories = EventCategory.objects.all()
    
    context = {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'date_filter': date_filter,
    }
    
    return render(request, 'events/event_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Prefetch photos for better performance
    event = Event.objects.prefetch_related('photos__user').get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Set the current user as organizer
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventCreationForm()
    
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user is the organizer
    if request.user != event.organizer:
        messages.error(request, 'You can only edit events that you organized.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        form = EventEditForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, f'Event "{event.title}" updated successfully!')
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventEditForm(instance=event)
    
    return render(request, 'events/edit_event.html', {'form': form, 'event': event})

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user is the organizer
    if request.user != event.organizer:
        messages.error(request, 'You can only delete events that you organized.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" has been deleted successfully.')
        return redirect('events:event_list')
    
    # If not POST, redirect to detail page
    return redirect('events:event_detail', event_id=event.id)