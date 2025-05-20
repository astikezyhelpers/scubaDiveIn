from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    ServiceCategory, DivingService, ServiceImage, DiveLocation,
    Event, RazorpayPayment, UserMessage, NewsletterSubscription,
    FAQ, InstructorBooking, Lead
)
from .forms import (
    DivingServiceForm, ServiceImageForm, ServiceCategoryForm
)

class ServiceImageInline(admin.TabularInline):
    model = ServiceImage
    extra = 1

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    form = ServiceCategoryForm
    list_display = ('name', 'order', 'image_preview')
    list_filter = ('order',)
    search_fields = ('name', 'description')
    ordering = ('order', 'name')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(DivingService)
class DivingServiceAdmin(admin.ModelAdmin):
    form = DivingServiceForm
    list_display = ('name', 'category', 'price', 'get_duration_display', 'is_featured', 'is_active', 'image_preview')
    list_filter = ('category', 'is_featured', 'is_active', 'difficulty_level', 'duration_unit')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceImageInline]
    ordering = ('category', 'name')

    def get_duration_display(self, obj):
        return obj.get_formatted_duration()
    get_duration_display.short_description = 'Duration'

    def image_preview(self, obj):
        if obj.featured_image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.featured_image)
        return "-"
    image_preview.short_description = 'Featured Image Preview'

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'short_description', 'description', 'featured_image')
        }),
        ('Course Details', {
            'fields': ('price', 'duration', 'duration_unit', 'max_participants', 'difficulty_level')
        }),
        ('Additional Information', {
            'fields': ('included_items', 'requirements')
        }),
        ('Course Variations', {
            'fields': ('variations',),
            'description': 'Add variations in JSON format. Example: [{"id": "shore", "name": "Shore DSD", "price": 5500, "duration": 180, "duration_unit": "minutes"}, {"id": "boat", "name": "Boat DSD", "price": 6500, "duration": 3, "duration_unit": "hours"}]'
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        }),
    )

@admin.register(ServiceImage)
class ServiceImageAdmin(admin.ModelAdmin):
    form = ServiceImageForm
    list_display = ('service', 'caption', 'order', 'image_preview')
    list_filter = ('service',)
    ordering = ('service', 'order')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image)
        return "-"
    image_preview.short_description = 'Image Preview'

@admin.register(DiveLocation)
class DiveLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'boat_ride_duration', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'location', 'price', 'is_featured', 'is_active')
    list_filter = ('location', 'is_featured', 'is_active', 'event_date')
    search_fields = ('name', 'description', 'location__name')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'event_date'

@admin.register(RazorpayPayment)
class RazorpayPaymentAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'payment_id', 'user', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'payment_id', 'user__email', 'customer_notes')
    readonly_fields = ('order_id', 'payment_id', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    date_hierarchy = 'subscribed_at'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('question', 'answer', 'category')
    ordering = ('order', 'category')

@admin.register(InstructorBooking)
class InstructorBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'instructor', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'instructor')
    search_fields = ('name', 'email', 'instructor', 'message')
    date_hierarchy = 'created_at'

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'course_interest', 'created_at', 'is_contacted')
    list_filter = ('is_contacted', 'subscribe_newsletter', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(is_contacted=True)
    mark_as_contacted.short_description = "Mark selected leads as contacted"
    
    actions = ['mark_as_contacted']
