from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import EventCreationForm, EventEditForm
from .models import Event, EventCategory
from search.models import Location
from interaction.models import EventParticipation
from search.models import SearchHistory
from django.db.models import Q, Count, Case, When, IntegerField, F
from django.utils import timezone
from datetime import timedelta

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    paginate_by = 6 
    
    def get_queryset(self):
        queryset = Event.objects.annotate(
            participant_count=Count('eventparticipation')
        ).select_related('category', 'organizer', 'location')
        
        # Get search parameters
        search_query = self.request.GET.get('search', '').strip()
        category_filter = self.request.GET.get('category', '').strip()
        date_filter = self.request.GET.get('date', '').strip()
        location_filter = self.request.GET.get('location', '').strip()
        date_range_filter = self.request.GET.get('date_range', '').strip()
        start_date = self.request.GET.get('start_date', '').strip()
        end_date = self.request.GET.get('end_date', '').strip()
        status_filter = self.request.GET.get('status', '').strip()
        availability_filter = self.request.GET.get('availability', '').strip()
        sort_filter = self.request.GET.get('sort', 'date').strip()
        
        # Keyword search
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(address_details__icontains=search_query) |
                Q(location__name__icontains=search_query) |
                Q(organizer__first_name__icontains=search_query) |
                Q(organizer__last_name__icontains=search_query)
            )
        
        # Category filter
        if category_filter:
            queryset = queryset.filter(category__name__iexact=category_filter)
        
        # Location filter - now using Location model
        if location_filter:
            queryset = queryset.filter(location__name__iexact=location_filter)
        
        # Specific date filter
        if date_filter:
            try:
                filter_date = timezone.datetime.strptime(date_filter, '%Y-%m-%d').date()
                queryset = queryset.filter(date_time__date=filter_date)
            except ValueError:
                pass
        
        # Date range filters
        if date_range_filter:
            now = timezone.now()
            if date_range_filter == 'today':
                queryset = queryset.filter(date_time__date=now.date())
            elif date_range_filter == 'week':
                start_week = now.date()
                end_week = start_week + timedelta(days=7)
                queryset = queryset.filter(date_time__date__range=[start_week, end_week])
            elif date_range_filter == 'month':
                start_month = now.date().replace(day=1)
                if start_month.month == 12:
                    end_month = start_month.replace(year=start_month.year + 1, month=1)
                else:
                    end_month = start_month.replace(month=start_month.month + 1)
                queryset = queryset.filter(date_time__date__range=[start_month, end_month])
            elif date_range_filter == 'custom' and start_date and end_date:
                try:
                    start_dt = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
                    end_dt = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
                    if start_dt <= end_dt:
                        queryset = queryset.filter(date_time__date__range=[start_dt, end_dt])
                except ValueError:
                    pass
        
        # Status filter
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Availability filter
        if availability_filter:
            if availability_filter == 'available':
                # Events with spots available
                queryset = queryset.annotate(
                    spots_available=Case(
                        When(participant_count__lt=F('max_participants'), then=1),
                        default=0,
                        output_field=IntegerField()
                    )
                ).filter(spots_available=1)
            elif availability_filter == 'full':
                # Full events
                queryset = queryset.filter(participant_count__gte=F('max_participants'))
        
        # Sorting
        if sort_filter == 'title':
            queryset = queryset.order_by('title')
        elif sort_filter == 'participants':
            queryset = queryset.order_by('-participant_count')
        elif sort_filter == 'created':
            queryset = queryset.order_by('-created_at')
        else:  # default: date
            queryset = queryset.order_by('date_time')
        
        # Save search history if user is authenticated and there's a search query
        if self.request.user.is_authenticated and search_query:
            SearchHistory.objects.create(
                user=self.request.user,
                search_query=search_query,
                results_count=queryset.count()
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Categories and locations for dropdown
        context['categories'] = EventCategory.objects.all()
        context['locations'] = Location.objects.all()
        
        # Pass all filter values back to template
        context['search_query'] = self.request.GET.get('search', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['date_filter'] = self.request.GET.get('date', '')
        context['location_filter'] = self.request.GET.get('location', '')
        context['date_range_filter'] = self.request.GET.get('date_range', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['availability_filter'] = self.request.GET.get('availability', '')
        context['sort_filter'] = self.request.GET.get('sort', 'date')
        
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
            Event.objects.prefetch_related('photos__user').select_related('location', 'category', 'organizer').annotate(
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
    
    # Pass categories and locations to template
    context = {
        'form': form,
        'categories': EventCategory.objects.all(),
        'locations': Location.objects.all()
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
    
    context = {
        'form': form, 
        'event': event,
        'locations': Location.objects.all()
    }
    
    return render(request, 'events/edit_event.html', context)

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