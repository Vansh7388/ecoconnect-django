from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date_time']