from django.contrib import admin
from .models import Location, EventTag, SearchHistory

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')

@admin.register(EventTag)
class EventTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_query', 'search_date', 'results_count')
    list_filter = ('search_date',)