from django import forms
from .models import UserMessage

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