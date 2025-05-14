import logging
from django.contrib import messages

logger = logging.getLogger(__name__)

class LoginAttemptMiddleware:
    """Middleware to handle login attempt logging and error messages"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if there's a login error
        if (request.method == 'POST' and 
            request.path == '/accounts/login/' and 
            not request.user.is_authenticated):
            
            # Add a more user-friendly message if there was a login error
            if 'form' in request.POST and hasattr(request, '_messages'):
                # Only add a message if no message with this text already exists
                existing_messages = [m.message for m in messages.get_messages(request)]
                
                if "Please check your username and password and try again." not in existing_messages:
                    messages.error(
                        request, 
                        "Please check your username and password and try again."
                    )
                    
                    # Log failed attempt without sensitive details
                    username = request.POST.get('username', '')
                    if username:
                        logger.warning(f"Failed login attempt for username: {username}")
        
        return response 