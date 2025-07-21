from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from events.models import Event
from django.utils import timezone

class HomeView(TemplateView):
    template_name = 'search/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['featured_events'] = Event.objects.filter(
            date_time__gte=timezone.now(),
            status='upcoming'
        ).order_by('date_time')[:3]
        
        context['total_events'] = Event.objects.count()
        context['upcoming_events'] = Event.objects.filter(status='upcoming').count()
        
        return context