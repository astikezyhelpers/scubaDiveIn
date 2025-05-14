import razorpay
import time
import json
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import RazorpayPayment, DivingService, ServiceCategory
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserMessage
import logging
from django.db import models

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def has_purchased_course(user, service, email=None):
    """Check if a user or email has already purchased a course"""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Checking purchase for service: {service.id} ({service.name})")
    
    # First check for authenticated user purchases
    if user and user.is_authenticated:
        logger.info(f"Checking if user {user.username} (ID: {user.id}) has purchased this course")
        # Check by user ID
        user_purchase = RazorpayPayment.objects.filter(
            user=user,
            service=service,
            status='completed'
        ).exists()
        
        if user_purchase:
            logger.info(f"User {user.username} has already purchased this course")
            return True
            
        # If user is logged in and has an email, also check email-based purchases 
        # that might have been made before the user account was created
        if email and user.email and email.lower() == user.email.lower():
            logger.info(f"User is authenticated with matching email {email}, performing additional checks")
    
    # Check for email-based purchases with a more precise search
    if email:
        email = email.strip().lower()
        logger.info(f"Checking if email {email} has purchased this course")
        
        # Search both case-insensitive exact matches and pattern matches
        email_purchases = RazorpayPayment.objects.filter(
            service=service,
            status='completed'
        ).filter(
            # Try different common patterns for storing email in customer_notes
            models.Q(customer_notes__icontains=f"Email: {email}") |
            models.Q(customer_notes__icontains=f"email: {email}") |
            models.Q(customer_notes__icontains=f"Email:{email}") |
            models.Q(customer_notes__icontains=f"Email: {email},") |
            models.Q(customer_notes__iregex=fr"[Ee]mail:?\s+{email}")
        )
        
        if email_purchases.exists():
            logger.info(f"Email {email} has already been used to purchase this course")
            return True
    
    logger.info(f"No previous purchase found for this user/email and course")
    return False

@login_required
def initiate_payment(request):
    service_id = request.GET.get('service_id')
    if not service_id:
        return redirect('courses')
    
    service = get_object_or_404(DivingService, id=service_id, is_active=True)
    
    # Check if user has already purchased this course
    already_purchased = has_purchased_course(request.user, service)
    
    if already_purchased:
        messages.warning(request, f"You have already purchased the '{service.name}' course. Check your booking history.")
        return redirect('booking_history')
    
    # Get user profile info for prefilling the form
    user = request.user
    context = {
        'service': service,
        'user_info': {
            'name': f"{user.first_name} {user.last_name}".strip(),
            'email': user.email,
            'phone': user.profile.phone_number if hasattr(user, 'profile') else '',
        },
        'is_authenticated': True
    }
    return render(request, 'mainSite/initiate_payment.html', context)

# Guest checkout version (no login required)
def guest_checkout(request):
    # Redirect authenticated users to regular checkout
    if request.user.is_authenticated:
        service_id = request.GET.get('service_id')
        if service_id:
            return redirect(f"{reverse('initiate_payment')}?service_id={service_id}")
        return redirect('courses')
    
    logger = logging.getLogger(__name__)
    
    service_id = request.GET.get('service_id')
    if not service_id:
        return redirect('courses')
    
    service = get_object_or_404(DivingService, id=service_id, is_active=True)
    
    # Add warning for guest users
    messages.warning(
        request, 
        "Note: If you're a returning user, please log in first to avoid duplicate purchases and to access your course history."
    )
    
    context = {
        'service': service,
        'is_authenticated': False,
        'warning_message': "Note: Purchasing without an account will make it harder to access your course materials later. Consider creating an account first."
    }
    return render(request, 'mainSite/initiate_payment.html', context)

@require_POST
def create_payment(request):
    try:
        data = json.loads(request.body)
        service_id = data.get('service_id')
        name = data.get('name')
        email = data.get('email', '').strip().lower() if data.get('email') else ''
        phone = data.get('phone')

        logger = logging.getLogger(__name__)
        logger.info(f"Payment creation requested for service_id={service_id}, email={email}")

        if not all([service_id, name, email, phone]):
            return JsonResponse({
                'success': False, 
                'error': 'Missing required fields'
            })

        service = get_object_or_404(DivingService, id=service_id, is_active=True)
        
        # Double check for any existing purchases with this email as a standalone check
        # This is a more direct check than relying on customer_notes
        existing_purchases = RazorpayPayment.objects.filter(
            service=service,
            status='completed'
        )
        
        # Find any matching email entries 
        if request.user.is_authenticated:
            user_purchases = existing_purchases.filter(user=request.user).exists()
            if user_purchases:
                logger.info(f"User {request.user.username} has already purchased this course (direct user check)")
                return JsonResponse({
                    'success': False,
                    'error': f"You have already purchased this course. Check your booking history.",
                    'redirect_to': reverse('booking_history')
                })

        # Extra check for email in customer_notes (pattern matching)
        import re
        for purchase in existing_purchases:
            if purchase.customer_notes:
                # Look for email patterns in customer_notes
                extracted_emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', purchase.customer_notes)
                for extracted_email in extracted_emails:
                    if extracted_email.lower() == email.lower():
                        logger.info(f"Email {email} was found in existing purchase (ID: {purchase.id})")
                        return JsonResponse({
                            'success': False,
                            'error': f"This email has already been used to purchase this course.",
                            'redirect_to': reverse('booking_history') if request.user.is_authenticated else reverse('courses')
                        })
        
        # Use the comprehensive check from the utility function as a fallback
        already_purchased = has_purchased_course(request.user, service, email)
        if already_purchased:
            logger.info(f"Duplicate purchase detected by has_purchased_course function")
            return JsonResponse({
                'success': False,
                'error': f"This course has already been purchased with this account or email. Check your booking history.",
                'redirect_to': reverse('booking_history') if request.user.is_authenticated else reverse('courses')
            })
        
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        
        # Create Razorpay order
        order_data = {
            'amount': int(service.price * 100),  # Amount in paise
            'currency': 'INR',
            'receipt': f'order_{service_id}_{int(time.time())}',
            'notes': {
                'service_id': service_id,
                'name': name,
                'email': email,
                'phone': phone
            }
        }
        
        try:
            order = client.order.create(data=order_data)
        except Exception as e:
            logger.error(f"Error creating Razorpay order: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Error creating Razorpay order: {str(e)}'
            })
        
        # Create payment record with standardized customer notes format
        try:
            customer_notes = f"Name: {name}, Email: {email}, Phone: {phone}"
            payment = RazorpayPayment.objects.create(
                service=service,
                order_id=order['id'],
                amount=service.price,
                customer_notes=customer_notes,
                # Associate with user if authenticated
                user=request.user if request.user.is_authenticated else None
            )
            logger.info(f"Payment record created: ID={payment.id}, order_id={order['id']}")
        except Exception as e:
            logger.error(f"Error creating payment record: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Error creating payment record: {str(e)}'
            })
        
        return JsonResponse({
            'success': True,
            'key_id': settings.RAZORPAY_KEY_ID,
            'amount': order['amount'],
            'currency': order['currency'],
            'order_id': order['id'],
            'name': name,
            'email': email,
            'phone': phone
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        })
    except Exception as e:
        logger.error(f"Unexpected error in create_payment: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })

def payment_success(request):
    payment_id = request.GET.get('payment_id')
    if not payment_id:
        return redirect('coursesPage')
    
    try:
        payment = RazorpayPayment.objects.get(payment_id=payment_id, status='completed')
        context = {
            'payment': payment,
            'service': payment.service
        }
        
        # If the user is logged in, show a link to booking history
        if request.user.is_authenticated:
            context['show_booking_history_link'] = True
            
        return render(request, 'mainSite/payment_success.html', context)
    except RazorpayPayment.DoesNotExist:
        # If payment not found or not completed, redirect to courses page
        return redirect('coursesPage')

@csrf_exempt
def payment_callback(request):
    logger = logging.getLogger(__name__)
    
    if request.method == 'POST':
        try:
            # Get the payment data from Razorpay
            payment_id = request.POST.get('razorpay_payment_id')
            order_id = request.POST.get('razorpay_order_id')
            signature = request.POST.get('razorpay_signature')
            
            logger.info(f"Payment callback received: order_id={order_id}, payment_id={payment_id}")
            
            # Verify the payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': order_id,
                'razorpay_signature': signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            logger.info(f"Payment signature verified for order_id={order_id}")
            
            # Update payment record
            payment = RazorpayPayment.objects.get(order_id=order_id)
            previous_status = payment.status
            payment.payment_id = payment_id
            
            # Standardize the customer_notes format for better email searching
            if payment.customer_notes and "Email:" not in payment.customer_notes:
                import re
                email_match = re.search(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', payment.customer_notes)
                if email_match:
                    email = email_match.group(1)
                    # Format the notes to have a standard "Email: email@example.com" pattern
                    if "Email:" not in payment.customer_notes:
                        payment.customer_notes = payment.customer_notes.replace(email, f"Email: {email}")
                    logger.info(f"Standardized email format in customer_notes: {email}")
            
            # If user is None but email exists and matches a user, associate the payment
            if payment.user is None and payment.customer_notes:
                import re
                email_match = re.search(r'Email:\s*([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', payment.customer_notes, re.IGNORECASE)
                if email_match:
                    email = email_match.group(1)
                    try:
                        user = User.objects.get(email__iexact=email)
                        payment.user = user
                        logger.info(f"Associated payment with user {user.username} based on email {email}")
                    except User.DoesNotExist:
                        logger.info(f"No user found with email {email}")
            
            payment.status = 'completed'
            payment.save()
            
            logger.info(f"Payment status updated from '{previous_status}' to 'completed' for order_id={order_id}")
            
            # Return success response
            return JsonResponse({
                'status': 'success',
                'message': 'Payment verified successfully',
                'redirect_url': f"{request.scheme}://{request.get_host()}/payment/success/?payment_id={payment_id}"
            })
            
        except Exception as e:
            logger.error(f"Payment callback error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def home(request):
    return render(request, 'mainSite/index.html')

def about(request):
    return render(request, 'mainSite/about-us.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Create message but don't save yet
            message = form.save(commit=False)
            
            # If user is authenticated, associate the message with the user
            if request.user.is_authenticated:
                message.user = request.user
            
            # Save the message
            message.save()
            
            # Send notification email to admin
            notify_admin_new_message(message)
            
            # Add success message
            messages.success(request, "Thank you for your message. We will get back to you soon!")
            
            # Redirect to the same page to avoid form resubmission
            return redirect('contact')
    else:
        # Pre-fill form if user is logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email
            }
        form = ContactForm(initial=initial_data)
    
    context = {
        'form': form
    }
    return render(request, 'mainSite/contact.html', context)

def notify_admin_new_message(message_obj):
    """Send email notification to admin about new message"""
    subject = f"New contact message from {message_obj.name}"
    email_body = f"""
    You have received a new message on ScubaDiveIn website.
    
    From: {message_obj.name} ({message_obj.email})
    Subject: {message_obj.subject or 'No subject'}
    Date: {message_obj.created_at.strftime('%Y-%m-%d %H:%M')}
    
    Message:
    {message_obj.message}
    
    You can view all messages in the admin panel.
    """
    
    try:
        send_mail(
            subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending admin notification: {str(e)}")

# Admin view to send message to a user
@login_required
def send_message_to_user(request, user_id):
    """Send a message to a specific user"""
    # Only staff/admin can access this view
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('home')
    
    try:
        recipient = User.objects.get(id=user_id)
        
        if request.method == 'POST':
            subject = request.POST.get('subject', '')
            message_body = request.POST.get('message', '')
            
            if not message_body:
                messages.error(request, "Message content is required.")
                return redirect('send_message_to_user', user_id=user_id)
            
            # Send email to the user
            email_body = f"""
            Hello {recipient.first_name or recipient.username},
            
            {message_body}
            
            Thanks,
            ScubaDiveIn Team
            """
            
            send_mail(
                subject or "Message from ScubaDiveIn",
                email_body,
                settings.EMAIL_HOST_USER,
                [recipient.email],
                fail_silently=False,
            )
            
            # Record the message in the database
            UserMessage.objects.create(
                name="ScubaDiveIn Admin",
                email=settings.EMAIL_HOST_USER,
                subject=subject,
                message=message_body,
                status='replied',
                user=recipient,
                admin_notes=f"Sent by {request.user.username}",
                reply_content=message_body,
                replied_at=timezone.now()
            )
            
            messages.success(request, f"Message sent successfully to {recipient.email}")
            return redirect('admin:index')  # Redirect to admin dashboard
        
        context = {
            'recipient': recipient
        }
        return render(request, 'admin/send_message.html', context)
    
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('admin:index')  # Redirect to admin dashboard

def courses(request):
    courses = DivingService.objects.filter(is_active=True).select_related('category')
    context = {
        'courses': courses,
    }
    return render(request, 'mainSite/courses.html', context)

def instructors(request):
    return render(request, 'mainSite/instructors.html')

def blogs(request):
    return render(request, 'mainSite/blogs.html')

def blogDetail(request,slug):
    return render(request, 'mainSite/blogDetail.html')

def sampleBlog(request):
    return render(request, 'mainSite/blogDetail.html')

def courseDetail(request, slug):
    try:
        course = DivingService.objects.get(slug=slug, is_active=True)
        
        # Check if authenticated user has already purchased this course
        already_purchased = has_purchased_course(request.user, course)
        
        context = {
            'course': course,
            'images': course.images.all().order_by('order'),
            'already_purchased': already_purchased
        }
        return render(request, 'mainSite/courseDetail.html', context)
    except DivingService.DoesNotExist:
        return redirect('coursesPage')

# Legal Pages Views
def privacy_policy(request):
    context = {
        'current_date': time.strftime("%B %d, %Y")
    }
    return render(request, 'mainSite/privacy-policy.html', context)

def terms_conditions(request):
    context = {
        'current_date': time.strftime("%B %d, %Y")
    }
    return render(request, 'mainSite/terms-and-conditions.html', context)

def shipping_policy(request):
    context = {
        'current_date': time.strftime("%B %d, %Y")
    }
    return render(request, 'mainSite/shipping-policy.html', context)

def cancellations_refunds(request):
    context = {
        'current_date': time.strftime("%B %d, %Y")
    }
    return render(request, 'mainSite/cancellations-refunds.html', context)