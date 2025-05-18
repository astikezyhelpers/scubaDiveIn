from django import forms
from .models import UserMessage, InstructorBooking
from django.core.validators import RegexValidator
from datetime import datetime

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
            'message': forms.Textarea(attrs={
                'class': 'flex w-full border-2 border-ocean-blue/20 bg-white p-3 placeholder:text-ocean-blue/50 focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50 min-h-[11.25rem] overflow-auto rounded-lg',
                'placeholder': 'Type your message...'
            })
        }

class InstructorBookingForm(forms.ModelForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date().isoformat()})
    )

    class Meta:
        model = InstructorBooking
        fields = ['name', 'email', 'phone', 'preferred_date', 'message', 'instructor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Your Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': 'Any specific requirements or questions?', 'rows': 4}),
            'instructor': forms.HiddenInput()
        } 