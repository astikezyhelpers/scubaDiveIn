from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.utils import timezone
from .utils.imagekit_field import ImageKitField

class ServiceCategory(models.Model):
    """Categories for scuba diving services"""
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    image = ImageKitField(folder_name='category_images', max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order on the website", db_index=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Service Categories"
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['order', 'name']),
        ]

class DivingService(models.Model):
    """Model for scuba diving services"""
    DIFFICULTY_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )
    
    DURATION_UNIT_CHOICES = (
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
    )
    
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, help_text="Base price or starting price")
    duration = models.PositiveIntegerField(help_text="Base duration value")
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default='minutes', help_text="Unit for the duration")
    max_participants = models.PositiveIntegerField(help_text="Maximum number of participants", default=4)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    included_items = models.TextField(blank=True, help_text="Base items included in the service, one per line")
    requirements = models.TextField(blank=True, help_text="Base requirements for this service, one per line")
    featured_image = ImageKitField(folder_name='service_images', max_length=500, blank=True, null=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    variations = models.JSONField(blank=True, null=True, help_text='Course variations stored as JSON. Format: [{"id": "str", "name": "str", "price": float, "duration": int, "max_participants": int}]')

    def has_variations(self):
        """Check if the service has any variations"""
        return bool(self.variations)

    def get_price_range(self):
        """Get the price range for the service including variations"""
        if not self.variations:
            return {'min_price': self.price, 'max_price': self.price}
        
        prices = [float(var['price']) for var in self.variations]
        prices.append(float(self.price))  # Include base price
        return {
            'min_price': min(prices),
            'max_price': max(prices)
        }

    def get_variation_by_id(self, variation_id):
        """Get a specific variation by its ID"""
        if not self.variations:
            return None
        
        for variation in self.variations:
            if str(variation['id']) == str(variation_id):
                return variation
        return None
        
    def get_formatted_duration(self, value=None, unit=None):
        """Get the duration formatted with the appropriate unit
        
        Args:
            value (int, optional): Duration value. Defaults to self.duration.
            unit (str, optional): Duration unit. Defaults to self.duration_unit.
            
        Returns:
            str: Formatted duration string with unit
        """
        duration = value if value is not None else self.duration
        duration_unit = unit if unit is not None else self.duration_unit
        
        if duration_unit == 'hours':
            if duration == 1:
                return f"{duration} hour"
            return f"{duration} hours"
        elif duration_unit == 'days':
            if duration == 1:
                return f"{duration} day"
            return f"{duration} days"
        else:  # minutes is the default
            return f"{duration} minutes"
            
    def get_variation_formatted_duration(self, variation):
        """Get the formatted duration for a variation
        
        Args:
            variation (dict): Variation dictionary with duration
            
        Returns:
            str: Formatted duration string with unit
        """
        # If the variation has a duration, use it, otherwise use the base duration
        duration = variation.get('duration', self.duration)
        
        # If the variation has a duration_unit, use it, otherwise use the base duration_unit
        duration_unit = variation.get('duration_unit', self.duration_unit)
        
        return self.get_formatted_duration(duration, duration_unit)

    class Meta:
        ordering = ['name']
        verbose_name = 'Diving Service'
        verbose_name_plural = 'Diving Services'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courseDetailPage', args=[self.slug])

class ServiceImage(models.Model):
    """Additional images for services"""
    service = models.ForeignKey(DivingService, on_delete=models.CASCADE, related_name='images')
    image = ImageKitField(folder_name='service_gallery', max_length=500)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Image for {self.service.name}"
    
    class Meta:
        ordering = ['order']

class DiveLocation(models.Model):
    """Model for dive locations/sites"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    featured_image = ImageKitField(folder_name='dive_locations', max_length=500, blank=True, null=True)
    boat_ride_duration = models.PositiveIntegerField(help_text="Duration in minutes")
    depth_range_min = models.PositiveIntegerField(help_text="Minimum depth in meters")
    depth_range_max = models.PositiveIntegerField(help_text="Maximum depth in meters")
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_featured', 'is_active']),
        ]
        verbose_name = "Dive Location"
        verbose_name_plural = "Dive Locations"

class Event(models.Model):
    """Model for diving events and activities"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    featured_image = ImageKitField(folder_name='event_images', max_length=500, blank=True, null=True)
    event_date = models.DateField(db_index=True)
    start_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    location = models.ForeignKey(DiveLocation, on_delete=models.CASCADE, related_name='events')
    max_participants = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    is_featured = models.BooleanField(default=False, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.event_date}"
    
    class Meta:
        ordering = ['event_date', 'start_time']
        indexes = [
            models.Index(fields=['is_featured', 'is_active']),
            models.Index(fields=['event_date', 'start_time']),
        ]
        verbose_name = "Event"
        verbose_name_plural = "Events"

class RazorpayPayment(models.Model):
    """Model to track Razorpay payments"""
    PAYMENT_STATUS_CHOICES = (
        ('created', 'Created'),
        ('attempted', 'Attempted'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments', null=True)
    service = models.ForeignKey(DivingService, on_delete=models.CASCADE, related_name='payments', null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='payments', null=True)
    order_id = models.CharField(max_length=100, db_index=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='created', db_index=True)
    booking_date = models.DateField(null=True, blank=True, db_index=True)
    participants = models.PositiveIntegerField(default=1)
    customer_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.service:
            return f"Payment {self.order_id} - Course: {self.service.name} - {self.status}"
        elif self.event:
            return f"Payment {self.order_id} - Event: {self.event.name} - {self.status}"
        return f"Payment {self.order_id} - {self.status}"
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['service', 'booking_date']),
            models.Index(fields=['event', 'booking_date']),
            models.Index(fields=['created_at']),
        ]

class UserMessage(models.Model):
    """Model to store messages from users"""
    STATUS_CHOICES = (
        ('unread', 'Unread'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # If the user was logged in when sending the message
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                             related_name='messages', null=True, blank=True)
    
    # For admin notes or reply content
    admin_notes = models.TextField(blank=True)
    reply_content = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Message from {self.name} - {self.created_at.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Message"
        verbose_name_plural = "User Messages"

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = 'Newsletter Subscription'
        verbose_name_plural = 'Newsletter Subscriptions'
    
    def __str__(self):
        return self.email

class FAQ(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question

class InstructorBooking(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('closed', 'Closed')
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    preferred_date = models.DateField(null=True, blank=True)
    message = models.TextField()
    instructor = models.CharField(max_length=100)  # Name of the instructor they want to book
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Instructor Booking'
        verbose_name_plural = 'Instructor Bookings'
    
    def __str__(self):
        return f"Booking by {self.name} for {self.instructor} on {self.preferred_date}"

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    course_interest = models.CharField(max_length=100, blank=True, null=True)
    subscribe_newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    is_contacted = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.email} ({self.created_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'