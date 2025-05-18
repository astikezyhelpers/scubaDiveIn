from django.contrib import admin
from .models import RazorpayPayment, ServiceCategory, DivingService, ServiceImage, UserMessage, DiveLocation, Event, NewsletterSubscription, FAQ, InstructorBooking
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

# Register your models here.
admin.site.register(RazorpayPayment)
admin.site.register(ServiceCategory)
admin.site.register(DivingService)
admin.site.register(ServiceImage)

@admin.register(DiveLocation)
class DiveLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'depth_range_min', 'depth_range_max', 'boat_ride_duration', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject_short', 'status', 'created_at', 'user_link', 'actions_buttons')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'user', 'created_at')
        }),
        ('Message Content', {
            'fields': ('subject', 'message', 'status')
        }),
        ('Admin Response', {
            'fields': ('admin_notes', 'reply_content', 'replied_at')
        }),
    )
    
    def subject_short(self, obj):
        if obj.subject:
            return obj.subject if len(obj.subject) < 50 else f"{obj.subject[:47]}..."
        return "(No subject)"
    subject_short.short_description = "Subject"
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "-"
    user_link.short_description = "User Account"
    
    def actions_buttons(self, obj):
        if obj.user and obj.status != 'replied':
            url = reverse('send_message_to_user', args=[obj.user.id])
            return format_html(
                '<a href="{}" class="button" style="background-color: #069; color: white; padding: 4px 8px; border-radius: 4px; text-decoration: none;">Reply</a>',
                url
            )
        return ""
    actions_buttons.short_description = "Actions"
    
    def mark_as_read(self, request, queryset):
        queryset.filter(status='unread').update(status='read')
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_archived(self, request, queryset):
        queryset.update(status='archived')
    mark_as_archived.short_description = "Archive selected messages"
    
    actions = [mark_as_read, mark_as_archived]
    
    def save_model(self, request, obj, form, change):
        if 'reply_content' in form.changed_data and obj.reply_content:
            # If reply content is added/changed, set the replied_at timestamp
            obj.replied_at = timezone.now()
            obj.status = 'replied'
        super().save_model(request, obj, form, change)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_date', 'start_time', 'location', 'price', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active', 'event_date', 'location')
    search_fields = ('name', 'short_description', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('event_date', 'start_time')

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)
    date_hierarchy = 'subscribed_at'
    list_per_page = 50
    
    actions = ['mark_active', 'mark_inactive']
    
    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected subscriptions as active"
    
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected subscriptions as inactive"

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer', 'category')
    ordering = ('order', 'created_at')
    list_editable = ('order', 'is_active')
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Organization', {
            'fields': ('category', 'order', 'is_active'),
            'classes': ('collapse',)
        })
    )

@admin.register(InstructorBooking)
class InstructorBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'instructor', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'instructor')
    search_fields = ('name', 'email', 'phone', 'instructor')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Booking Details', {
            'fields': ('instructor', 'preferred_date', 'message')
        }),
        ('Status Information', {
            'fields': ('status', 'created_at')
        }),
    )
