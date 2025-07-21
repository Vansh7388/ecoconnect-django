from django import forms
from .models import PhotoUpload, EventParticipation

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = PhotoUpload
        fields = ('image', 'caption')
        widgets = {
            'caption': forms.TextInput(attrs={'placeholder': 'Photo caption (optional)...'}),
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class EventFeedbackForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ('feedback', 'attended')
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        }

class RSVPForm(forms.Form):
    confirm = forms.BooleanField(required=True, label="I want to join this event")
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))