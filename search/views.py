from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from django.db.models import Q, Count
from events.models import Event, EventCategory
from .models import Location, SearchHistory
from .forms import AdvancedSearchForm, QuickSearchForm
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

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

class AdvancedSearchView(TemplateView):
    template_name = 'search/advanced_search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdvancedSearchForm()
        context['categories'] = EventCategory.objects.all()
        context['locations'] = Location.objects.all()
        return context

class SearchResultsView(ListView):
    model = Event
    template_name = 'search/search_results.html'
    context_object_name = 'events'
    paginate_by = 10
    
    def get_queryset(self):
        form = AdvancedSearchForm(self.request.GET)
        queryset = Event.objects.all().order_by('-date_time')
        
        if form.is_valid():
            keywords = form.cleaned_data.get('keywords')
            category = form.cleaned_data.get('category')
            location = form.cleaned_data.get('location')
            date_range = form.cleaned_data.get('date_range')
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            
            # Keyword search
            if keywords:
                queryset = queryset.filter(
                    Q(title__icontains=keywords) |
                    Q(description__icontains=keywords) |
                    Q(location__icontains=keywords)
                )
            
            # Category filter
            if category:
                queryset = queryset.filter(category=category)
            
            # Location filter
            if location:
                queryset = queryset.filter(location__icontains=location.name)
            
            # Date range filter
            if date_range == 'today':
                queryset = queryset.filter(date_time__date=timezone.now().date())
            elif date_range == 'week':
                start_week = timezone.now().date()
                end_week = start_week + timezone.timedelta(days=7)
                queryset = queryset.filter(date_time__date__range=[start_week, end_week])
            elif date_range == 'month':
                start_month = timezone.now().date().replace(day=1)
                if start_month.month == 12:
                    end_month = start_month.replace(year=start_month.year + 1, month=1)
                else:
                    end_month = start_month.replace(month=start_month.month + 1)
                queryset = queryset.filter(date_time__date__range=[start_month, end_month])
            elif date_range == 'custom' and start_date and end_date:
                queryset = queryset.filter(date_time__date__range=[start_date, end_date])
        
        # Save search history if user is authenticated
        if self.request.user.is_authenticated:
            keywords = self.request.GET.get('keywords', '')
            if keywords:
                SearchHistory.objects.create(
                    user=self.request.user,
                    search_query=keywords,
                    results_count=queryset.count()
                )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AdvancedSearchForm(self.request.GET)
        context['search_query'] = self.request.GET.get('keywords', '')
        context['total_results'] = self.get_queryset().count()
        return context

class AnalyticsView(LoginRequiredMixin, TemplateView):
    template_name = 'search/analytics.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Event statistics
        context['total_events'] = Event.objects.count()
        context['upcoming_events'] = Event.objects.filter(status='upcoming').count()
        context['completed_events'] = Event.objects.filter(status='completed').count()
        
        # Category statistics
        context['category_stats'] = EventCategory.objects.annotate(
            event_count=Count('event')
        ).order_by('-event_count')
        
        # Recent search queries
        if self.request.user.is_authenticated:
            context['recent_searches'] = SearchHistory.objects.filter(
                user=self.request.user
            ).order_by('-search_date')[:10]
        
        # Popular search terms
        context['popular_searches'] = SearchHistory.objects.values('search_query').annotate(
            count=Count('search_query')
        ).order_by('-count')[:5]
        
        return context