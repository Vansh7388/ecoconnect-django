from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from events.models import Event

class EventParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(default=timezone.now)
    attended = models.BooleanField(default=False)
    feedback = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    
    class Meta:
        unique_together = ('user', 'event')

class PhotoUpload(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_photos/')
    caption = models.CharField(max_length=200, blank=True)
    upload_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Photo by {self.user.username} for {self.event.title}"
    
    class Meta:
        ordering = ['-upload_date']

class UserHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page_visited = models.CharField(max_length=200)
    visit_date = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} visited {self.page_visited}"
    
    class Meta:
        ordering = ['-visit_date']