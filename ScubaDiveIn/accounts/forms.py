from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_number', 'address', 'date_of_birth', 
                  'emergency_contact_name', 'emergency_contact_number',
                  'diving_experience', 'certification_level', 
                  'certification_agency', 'certification_number')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'diving_experience': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3})
        }

class CustomAuthenticationForm(AuthenticationForm):
    """Custom authentication form with better error messages"""
    error_messages = {
        'invalid_login': "Please enter a correct username and password. Note that both fields may be case-sensitive.",
        'inactive': "This account is inactive. Please contact support.",
    }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full px-4 py-2 border border-ocean-blue rounded-lg focus:ring-2 focus:ring-ocean-blue focus:border-transparent'})
        self.fields['password'].widget.attrs.update({'class': 'w-full px-4 py-2 border border-ocean-blue rounded-lg focus:ring-2 focus:ring-ocean-blue focus:border-transparent'})
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Add logging for authentication failures
        if self._errors:
            username = self.cleaned_data.get('username')
            if username:
                # Log failed login attempt (avoid logging password attempts)
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Failed login attempt for username: {username}")
        
        return cleaned_data 