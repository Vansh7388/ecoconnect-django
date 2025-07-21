from django.contrib import admin
from .models import EventParticipation, PhotoUpload, UserHistory

@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'joined_date', 'attended')
    list_filter = ('attended', 'joined_date')

@admin.register(PhotoUpload)
class PhotoUploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'upload_date')
    list_filter = ('upload_date',)

@admin.register(UserHistory)
class UserHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'page_visited', 'visit_date')
    list_filter = ('visit_date',)