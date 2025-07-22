from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from search.models import Location, EventTag

class EventCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=200)
    color_code = models.CharField(max_length=7, default="#28a745", help_text="Hex color code")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Event Categories"

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='events')
    address_details = models.CharField(max_length=200, blank=True, help_text="Specific address or landmark")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    tags = models.ManyToManyField(EventTag, blank=True, help_text="Select relevant tags for this event")
    max_participants = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    
    def __str__(self):
        return self.title
    
    def full_location(self):
        if self.address_details:
            return f"{self.address_details}, {self.location.name}"
        return self.location.name
    
    def get_tags_list(self):
        """Return a list of tag names for this event"""
        return list(self.tags.values_list('name', flat=True))
    
    class Meta:
        ordering = ['-date_time']