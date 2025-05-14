from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', 
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            authentication_form=CustomAuthenticationForm,
            redirect_authenticated_user=True,
            extra_context={'title': 'Login'}
        ), 
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='homePage'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.booking_history, name='booking_history'),
    
    # Custom OTP-based password reset URLs
    path('password-reset/', views.password_reset_request, name='password_reset'),
    path('password-reset/sent/', views.password_reset_sent, name='password_reset_sent'),
    path('password-reset/verify-otp/', views.password_reset_verify_otp, name='password_reset_verify_otp'),
    path('password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete, name='password_reset_complete'),
    
    # Password change URLs
    path('password-change/', 
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change.html'
        ),
        name='password_change'),
    path('password-change/done/', 
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done'),
] 