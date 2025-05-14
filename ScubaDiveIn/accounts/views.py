from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlencode
from django.contrib.auth.hashers import make_password
from .forms import SignUpForm, UserForm, ProfileForm
from .models import ResetPasswordOTP
import logging

logger = logging.getLogger(__name__)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user_form.save()
                profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def booking_history(request):
    # Get user's booking history
    bookings = request.user.payments.all().order_by('-created_at')
    
    # Calculate total spent on completed bookings
    total_spent = bookings.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    return render(request, 'accounts/booking_history.html', {
        'bookings': bookings,
        'total_spent': total_spent
    }) 

# Password Reset Views with OTP
def password_reset_request(request):
    """Handle the initial password reset request"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            messages.error(request, "Please enter a valid email address.")
            return render(request, 'accounts/password_reset.html')
        
        # Log the email for debugging    
        logger.info(f"Password reset requested for email: {email}")
            
        try:
            user = User.objects.get(email=email)
            # Generate OTP
            otp_obj = ResetPasswordOTP.generate_otp(user)
            
            # Log OTP generation
            logger.info(f"OTP generated for user {user.username}: {otp_obj.otp}")
            
            # Send email with OTP
            reset_url = request.build_absolute_uri(
                reverse('password_reset_verify_otp') + '?' + urlencode({'email': email})
            )
            
            email_body = f"""
            Hello {user.first_name or user.username},
            
            You requested a password reset for your ScubaDiveIn account.
            Your OTP is: {otp_obj.otp}
            
            Please use this OTP to reset your password. It is valid for 10 minutes.
            
            You can enter this OTP at: {reset_url}
            
            If you did not request this password reset, please ignore this email.
            
            Thanks,
            ScubaDiveIn Team
            """
            
            # Log email attempt
            logger.info(f"Attempting to send password reset email to: {email}")
            
            # Send the email
            try:
                sent = send_mail(
                    'ScubaDiveIn Password Reset OTP',
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                logger.info(f"Email send result: {sent}")
            except Exception as email_error:
                logger.error(f"Email sending error: {str(email_error)}")
                # Continue with the process even if email fails in development
            
            # Store email in session for verification
            request.session['reset_email'] = email
            
            # Show OTP on console in development mode
            if settings.DEBUG and settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
                print("\n----- DEBUG: PASSWORD RESET OTP -----")
                print(f"Email: {email}")
                print(f"OTP: {otp_obj.otp}")
                print("------------------------------------\n")
            
            return redirect('password_reset_sent')
        except User.DoesNotExist:
            # Still redirect to prevent email enumeration attacks
            # Store email in session for verification
            logger.info(f"Password reset attempted for non-existent email: {email}")
            request.session['reset_email'] = email
            return redirect('password_reset_sent')
        except Exception as e:
            logger.error(f"Error in password reset process: {str(e)}")
            messages.error(request, "An error occurred. Please try again later.")
    
    return render(request, 'accounts/password_reset.html')

def password_reset_sent(request):
    """Show a page confirming the password reset email was sent"""
    # Get the email from session if available
    email = request.session.get('reset_email', '')
    # Fix the handling of None values
    if email is None or email == 'None' or not email:
        email = ''
    
    # Pass debug flag to the template
    context = {
        'email': email,
        'debug': settings.DEBUG
    }
    
    return render(request, 'accounts/password_reset_done.html', context)

def password_reset_verify_otp(request):
    """Verify the OTP entered by the user"""
    # Get email from GET, POST or session
    email = request.GET.get('email') or request.POST.get('email')
    
    # Handle None, 'None' or empty values
    if email is None or email == 'None' or email == '':
        # Try to get from session
        if 'reset_email' in request.session:
            email = request.session.get('reset_email', '')
            if email is None or email == 'None' or email == '':
                email = ''
    
    # Log the email for debugging
    logger.info(f"OTP verification page for email: {email}")
    
    if not email:
        messages.error(request, "Email is required. Please try the password reset process again.")
        return redirect('password_reset')
    
    if request.method == 'POST':
        otp = request.POST.get('otp', '').strip()
        
        # Log OTP input for debugging
        logger.info(f"OTP verification attempt with code: {otp} for email: {email}")
        
        try:
            user = User.objects.get(email=email)
            otp_obj = ResetPasswordOTP.objects.filter(
                user=user, 
                otp=otp, 
                is_used=False
            ).order_by('-created_at').first()
            
            if otp_obj and otp_obj.is_valid():
                # Store the OTP in session for password reset confirmation
                request.session['verified_otp_id'] = otp_obj.id
                logger.info(f"OTP verification successful for user: {user.username}")
                return redirect('password_reset_confirm')
            else:
                logger.warning(f"Invalid or expired OTP for user: {user.username}")
                messages.error(request, "Invalid or expired OTP. Please try again.")
        except User.DoesNotExist:
            logger.warning(f"OTP verification attempt for non-existent email: {email}")
            messages.error(request, "User with this email does not exist.")
    
    return render(request, 'accounts/password_reset_verify_otp.html', {'email': email})

def password_reset_confirm(request):
    """Allow the user to set a new password after OTP verification"""
    otp_id = request.session.get('verified_otp_id')
    
    if not otp_id:
        messages.error(request, "OTP verification required.")
        return redirect('password_reset')
    
    try:
        otp_obj = ResetPasswordOTP.objects.get(id=otp_id, is_used=False)
        
        if not otp_obj.is_valid():
            messages.error(request, "OTP has expired. Please start over.")
            return redirect('password_reset')
            
        if request.method == 'POST':
            # Extract password values
            password1 = request.POST.get('new_password1', '')
            password2 = request.POST.get('new_password2', '')
            
            # Log attempt (excluding actual passwords)
            logger.info(f"Password reset confirmation attempt for user: {otp_obj.user.username}")
            
            # Basic validation
            if not password1 or not password2:
                messages.error(request, "Both password fields are required.")
                return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
                
            if password1 != password2:
                messages.error(request, "The two password fields didn't match.")
                return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
                
            if len(password1) < 8:
                messages.error(request, "Password must be at least 8 characters long.")
                return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
            
            try:
                # Update user's password
                user = otp_obj.user
                user.password = make_password(password1)
                user.save()
                
                # Mark OTP as used
                otp_obj.is_used = True
                otp_obj.save()
                
                # Clear session data
                if 'verified_otp_id' in request.session:
                    del request.session['verified_otp_id']
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                
                logger.info(f"Password reset successful for user: {user.username}")
                return redirect('password_reset_complete')
            except Exception as e:
                logger.error(f"Error during password update: {str(e)}")
                messages.error(request, "An error occurred while updating your password. Please try again.")
                return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
        else:
            # GET request, just show the form
            return render(request, 'accounts/password_reset_confirm.html', {'validlink': True})
        
    except ResetPasswordOTP.DoesNotExist:
        logger.warning(f"Invalid OTP verification during password reset confirm")
        messages.error(request, "Invalid OTP verification.")
        return redirect('password_reset')

def password_reset_complete(request):
    """Show a confirmation that the password has been reset"""
    return render(request, 'accounts/password_reset_complete.html') 