from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import EventCreationForm, EventEditForm
from .models import Event, EventCategory
from interaction.models import EventParticipation
from django.db.models import Q, Count
from django.utils import timezone

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.annotate(
            participant_count=Count('eventparticipation')
        ).order_by('date_time')
        
        search_query = self.request.GET.get('search')
        category_filter = self.request.GET.get('category')
        date_filter = self.request.GET.get('date')
        
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        if category_filter:
            queryset = queryset.filter(category__name__icontains=category_filter)
        
        if date_filter:
            queryset = queryset.filter(date_time__date=date_filter)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = EventCategory.objects.all()
        context['search_query'] = self.request.GET.get('search')
        context['category_filter'] = self.request.GET.get('category')
        context['date_filter'] = self.request.GET.get('date')
        
        # Add user participation status for each event
        if self.request.user.is_authenticated:
            user_participations = EventParticipation.objects.filter(
                user=self.request.user
            ).values_list('event_id', flat=True)
            context['user_participations'] = list(user_participations)
        else:
            context['user_participations'] = []
            
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    
    def get_object(self):
        return get_object_or_404(
            Event.objects.prefetch_related('photos__user').annotate(
                participant_count=Count('eventparticipation')
            ), 
            id=self.kwargs['event_id']
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        
        # Check if current user has joined this event
        if self.request.user.is_authenticated:
            context['user_joined'] = EventParticipation.objects.filter(
                user=self.request.user, 
                event=event
            ).exists()
        else:
            context['user_joined'] = False
            
        # Get participants list
        context['participants'] = EventParticipation.objects.filter(
            event=event
        ).select_related('user')[:10]  # Show first 10 participants
        
        # Check if event is full
        context['is_full'] = event.participant_count >= event.max_participants
        
        return context

@login_required
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user already joined
    if EventParticipation.objects.filter(user=request.user, event=event).exists():
        messages.warning(request, 'You have already joined this event.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if event is full
    current_participants = EventParticipation.objects.filter(event=event).count()
    if current_participants >= event.max_participants:
        messages.error(request, 'This event is full.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Check if event is in the past
    if event.date_time <= timezone.now():
        messages.error(request, 'Cannot join past events.')
        return redirect('events:event_detail', event_id=event.id)
    
    # Join the event
    EventParticipation.objects.create(user=request.user, event=event)
    messages.success(request, f'You have successfully joined "{event.title}"!')
    
    return redirect('events:event_detail', event_id=event.id)

@login_required
def leave_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    try:
        participation = EventParticipation.objects.get(user=request.user, event=event)
        participation.delete()
        messages.success(request, f'You have left "{event.title}".')
    except EventParticipation.DoesNotExist:
        messages.error(request, 'You are not registered for this event.')
    
    return redirect('events:event_detail', event_id=event.id)

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, f'Event "{event.title}" created successfully!')
            return redirect('events:event_detail', event_id=event.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EventCreationForm()
    
    # Pass categories to template
    context = {
        'form': form,
        'categories': EventCategory.objects.all()
    }
    
    return render(request, 'events/create_event.html', context)

@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
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
    
    if request.user != event.organizer:
        messages.error(request, 'You can only delete events that you organized.')
        return redirect('events:event_detail', event_id=event.id)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" has been deleted successfully.')
        return redirect('events:event_list')
    
    return redirect('events:event_detail', event_id=event.id)