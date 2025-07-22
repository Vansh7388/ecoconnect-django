from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    def __str__(self):
        return self.name

class EventTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, blank=True)
    color_code = models.CharField(max_length=7, default='#6c757d', help_text="Hex color code for the tag")
    
    def __str__(self):
        return self.name

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    search_query = models.CharField(max_length=200)
    search_date = models.DateTimeField(default=timezone.now)
    results_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Search: {self.search_query}"
    
    class Meta:
        ordering = ['-search_date']
        verbose_name_plural = "Search Histories"