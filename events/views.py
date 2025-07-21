from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import EventCreationForm
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

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Set the current user as organizer
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('events:event_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventCreationForm()
    
    return render(request, 'events/create_event.html', {'form': form})