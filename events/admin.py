from django.contrib import admin
from .models import Event, EventCategory

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_code')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'category', 'date_time', 'status')
    list_filter = ('status', 'category', 'date_time')
    search_fields = ('title', 'location')