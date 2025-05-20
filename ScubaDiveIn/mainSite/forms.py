from django import forms
from django.core.validators import RegexValidator
from datetime import datetime
from .models import (
    UserMessage, InstructorBooking, DivingService, 
    ServiceImage, ServiceCategory, Lead
)

class ContactForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'rounded-full flex size-full py-2 align-middle transition-all duration-200 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 border-2 border-ocean-blue/20 bg-white min-h-11 px-3',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'rounded-full flex size-full py-2 align-middle transition-all duration-200 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 border-2 border-ocean-blue/20 bg-white min-h-11 px-3',
                'placeholder': 'Your email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'rounded-full flex size-full py-2 align-middle transition-all duration-200 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 border-2 border-ocean-blue/20 bg-white min-h-11 px-3',
                'placeholder': 'Subject (optional)'
            }),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class DivingServiceForm(forms.ModelForm):
    class Meta:
        model = DivingService
        fields = '__all__'
        widgets = {
            'featured_image': forms.FileInput(),
            'description': forms.Textarea(attrs={'rows': 6}),
            'included_items': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter items one per line'}),
            'requirements': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter requirements one per line'}),
            'variations': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter variations in JSON format'}),
        }

class ServiceImageForm(forms.ModelForm):
    class Meta:
        model = ServiceImage
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(),
        }

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = '__all__'
        widgets = {
            'image': forms.FileInput(),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class InstructorBookingForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    
    class Meta:
        model = InstructorBooking
        fields = ['name', 'email', 'phone', 'preferred_date', 'message', 'instructor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Phone Number'}),
            'preferred_date': forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date().isoformat()}),
            'message': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_preferred_date(self):
        date = self.cleaned_data.get('preferred_date')
        if date and date < datetime.now().date():
            raise forms.ValidationError("The preferred date cannot be in the past.")
        return date 

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'message', 'course_interest', 'subscribe_newsletter']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-wave focus:border-ocean-blue focus:ring-2 focus:ring-ocean-blue/20 transition-all duration-300 outline-none text-deep-blue',
                'placeholder': 'John Doe'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-wave focus:border-ocean-blue focus:ring-2 focus:ring-ocean-blue/20 transition-all duration-300 outline-none text-deep-blue',
                'placeholder': 'john@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-wave focus:border-ocean-blue focus:ring-2 focus:ring-ocean-blue/20 transition-all duration-300 outline-none text-deep-blue',
                'placeholder': '+91 1234567890'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border-2 border-wave focus:border-ocean-blue focus:ring-2 focus:ring-ocean-blue/20 transition-all duration-300 outline-none text-deep-blue resize-none',
                'placeholder': 'Tell us about your diving interests and any questions you have...',
                'rows': '4'
            }),
            'course_interest': forms.HiddenInput(),
            'subscribe_newsletter': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-2 border-wave text-ocean-blue focus:ring-ocean-blue/20'
            })
        } 