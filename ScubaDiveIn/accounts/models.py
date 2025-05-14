from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta

class UserProfile(models.Model):
    """Extended user profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True)
    diving_experience = models.TextField(blank=True, help_text="Brief description of diving experience")
    certification_level = models.CharField(max_length=100, blank=True)
    certification_agency = models.CharField(max_length=100, blank=True)
    certification_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class ResetPasswordOTP(models.Model):
    """Model for password reset using OTP"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"OTP for {self.user.email}"
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_used and datetime.now().astimezone() < self.expires_at
    
    @classmethod
    def generate_otp(cls, user):
        """Generate a new OTP for the user"""
        # Invalidate any existing OTPs for this user
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        
        # Generate a new 6-digit OTP
        otp = ''.join(random.choices('0123456789', k=6))
        
        # Create and return a new OTP object (valid for 10 minutes)
        expires_at = datetime.now().astimezone() + timedelta(minutes=10)
        return cls.objects.create(user=user, otp=otp, expires_at=expires_at) 