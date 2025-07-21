from django import forms
from .models import Event, EventCategory
from django.utils import timezone

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date_time', 'location', 'category', 'max_participants')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title...'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your environmental event...'}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event location address...'}),
            'max_participants': forms.NumberInput(attrs={'min': 1, 'max': 1000, 'value': 50}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select Category"
        # Make date_time required and set minimum to current time
        self.fields['date_time'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

class EventEditForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'date_time', 'location', 'max_participants', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event title...'}),
            'description': forms.Textarea(attrs={'rows': 5}),
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event location address...'}),
            'max_participants': forms.NumberInput(attrs={'min': 1, 'max': 1000}),
        }

class EventSearchForm(forms.Form):
    query = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search events...'}))
    category = forms.ModelChoiceField(queryset=EventCategory.objects.all(), required=False, empty_label="All Categories")
    location = forms.CharField(max_length=100, required=False,widget=forms.TextInput(attrs={'placeholder': 'Location...'}))
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))