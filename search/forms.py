from django import forms
from events.models import EventCategory
from .models import Location

class AdvancedSearchForm(forms.Form):
    keywords = forms.CharField(max_length=200, required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Keywords...'}))
    category = forms.ModelChoiceField(queryset=EventCategory.objects.all(), 
                                    required=False, empty_label="Any Category")
    location = forms.ModelChoiceField(queryset=Location.objects.all(),
                                    required=False, empty_label="Any Location")
    date_range = forms.ChoiceField(choices=[
        ('', 'Any Time'),
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('custom', 'Custom Range'),
    ], required=False)
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    
class QuickSearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False,
                       widget=forms.TextInput(attrs={
                           'placeholder': 'Search events, locations...',
                           'class': 'form-control'
                       }))

class FilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=EventCategory.objects.all(),
                                    required=False, empty_label="Filter by Category")
    sort_by = forms.ChoiceField(choices=[
        ('date', 'Date'),
        ('title', 'Title'),
        ('participants', 'Participants'),
        ('created', 'Recently Added'),
    ], required=False, initial='date')