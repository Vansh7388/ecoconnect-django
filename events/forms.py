from django import forms
from .models import Event, EventCategory
from search.models import Location
from django.utils import timezone
from datetime import timedelta

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date_time', 'location', 'address_details', 'category', 'max_participants')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title...', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your environmental event...', 'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'address_details': forms.TextInput(attrs={'placeholder': 'Specific address or landmark...', 'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'min': 1, 'max': 1000, 'value': 50, 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"
        self.fields['location'].empty_label = "Select Location"
        # Set minimum date dynamically
        now = timezone.now()
        min_datetime = now.strftime('%Y-%m-%dT%H:%M')
        self.fields['date_time'].widget.attrs['min'] = min_datetime
    
    def clean_date_time(self):
        date_time = self.cleaned_data['date_time']
        now = timezone.now()
        
        # Check if date is in the past
        if date_time <= now:
            raise forms.ValidationError("Event cannot be scheduled in the past.")
        
        # Check if date is too far in the future (max 1 year)
        max_future = now + timedelta(days=365)
        if date_time > max_future:
            raise forms.ValidationError("Event cannot be scheduled more than 1 year in advance.")
        
        return date_time
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title.strip()) < 5:
            raise forms.ValidationError("Event title must be at least 5 characters long.")
        return title.strip()
    
    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description.strip()) < 20:
            raise forms.ValidationError("Event description must be at least 20 characters long.")
        return description.strip()
    
    def clean_address_details(self):
        address_details = self.cleaned_data.get('address_details', '')
        if address_details and len(address_details.strip()) < 5:
            raise forms.ValidationError("Address details must be at least 5 characters long.")
        return address_details.strip() if address_details else ''

class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date_time', 'location', 'address_details', 'max_participants', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title...', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'address_details': forms.TextInput(attrs={'placeholder': 'Specific address or landmark...', 'class': 'form-control'}),
            'max_participants': forms.NumberInput(attrs={'min': 1, 'max': 1000, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_date_time(self):
        date_time = self.cleaned_data['date_time']
        now = timezone.now()
        
        # Allow past dates for completed events, but warn for upcoming events
        if self.cleaned_data.get('status') == 'upcoming' and date_time <= now:
            raise forms.ValidationError("Upcoming events cannot be scheduled in the past.")
        
        return date_time
    
    def clean_max_participants(self):
        max_participants = self.cleaned_data['max_participants']
        
        # Check if reducing capacity below current registrations
        if self.instance:
            current_registrations = self.instance.eventparticipation_set.count()
            if max_participants < current_registrations:
                raise forms.ValidationError(
                    f"Cannot reduce capacity below current registrations ({current_registrations})."
                )
        
        return max_participants

class EventSearchForm(forms.Form):
    query = forms.CharField(
        max_length=200, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Search events...', 'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=EventCategory.objects.all(), 
        required=False, 
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(), 
        required=False,
        empty_label="All Locations",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    date_to = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError("Start date cannot be after end date.")
        
        return cleaned_data