from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import EventCreationForm, EventEditForm
from .models import Event, EventCategory
from django.db.models import Q

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.html'
    context_object_name = 'events'
    
    def get_queryset(self):
        queryset = Event.objects.all().order_by('date_time')
        
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
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'
    pk_url_kwarg = 'event_id'
    
    def get_object(self):
        return get_object_or_404(Event.objects.prefetch_related('photos__user'), id=self.kwargs['event_id'])

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
    
    return render(request, 'events/create_event.html', {'form': form})

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