from django import forms
from .models import PhotoUpload, EventParticipation
from PIL import Image
import os

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = PhotoUpload
        fields = ('image', 'caption')
        widgets = {
            'caption': forms.TextInput(attrs={
                'placeholder': 'Photo caption (optional)...', 
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'accept': 'image/*', 
                'class': 'form-control'
            }),
        }
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError("Image file size cannot exceed 5MB.")
            
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Please upload a valid image file (JPG, PNG, GIF, WebP).")
            
            # Validate image using PIL
            try:
                img = Image.open(image)
                img.verify()  # Verify it's a valid image
                
                # Reset file pointer after verify()
                image.seek(0)
                
                # Check image dimensions (min 100x100, max 4000x4000)
                img = Image.open(image)
                width, height = img.size
                
                if width < 100 or height < 100:
                    raise forms.ValidationError("Image must be at least 100x100 pixels.")
                
                if width > 4000 or height > 4000:
                    raise forms.ValidationError("Image dimensions cannot exceed 4000x4000 pixels.")
                
            except Exception:
                raise forms.ValidationError("Invalid image file. Please upload a valid image.")
            
            # Reset file pointer
            image.seek(0)
        
        return image
    
    def clean_caption(self):
        caption = self.cleaned_data.get('caption', '')
        if caption and len(caption.strip()) > 200:
            raise forms.ValidationError("Caption cannot exceed 200 characters.")
        return caption.strip() if caption else ''

class EventFeedbackForm(forms.ModelForm):
    class Meta:
        model = EventParticipation
        fields = ('feedback', 'attended')
        widgets = {
            'feedback': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Share your experience...',
                'class': 'form-control'
            }),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_feedback(self):
        feedback = self.cleaned_data.get('feedback', '')
        if feedback and len(feedback.strip()) < 10:
            raise forms.ValidationError("Feedback must be at least 10 characters long.")
        if feedback and len(feedback.strip()) > 500:
            raise forms.ValidationError("Feedback cannot exceed 500 characters.")
        return feedback.strip() if feedback else ''

class RSVPForm(forms.Form):
    confirm = forms.BooleanField(
        required=True, 
        label="I want to join this event",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your full name',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'your.email@example.com',
            'class': 'form-control'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Subject of your message',
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Your message...',
            'class': 'form-control'
        })
    )
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name.strip()
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message.strip()) < 20:
            raise forms.ValidationError("Message must be at least 20 characters long.")
        return message.strip()