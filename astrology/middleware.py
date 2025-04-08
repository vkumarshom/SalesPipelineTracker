import re
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class PhoneVerificationMiddleware:
    """
    Middleware to ensure users have verified their phone number via OTP
    before accessing certain pages.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require phone verification
        self.exempt_urls = [
            re.compile(r'^/admin/.*$'),
            re.compile(r'^/accounts/login/$'),
            re.compile(r'^/accounts/signup/$'),
            re.compile(r'^/accounts/logout/$'),
            re.compile(r'^/accounts/password/.*$'),
            re.compile(r'^/accounts/social/.*$'),
            re.compile(r'^/verify-otp/$'),
            re.compile(r'^/resend-otp/$'),
            re.compile(r'^/$'),
            re.compile(r'^/about/$'),
            re.compile(r'^/contact/$'),
            re.compile(r'^/blog/$'),
            re.compile(r'^/blog/.*$'),
            re.compile(r'^/services/$'),
            re.compile(r'^/services/.*$'),
            re.compile(r'^/static/.*$'),
            re.compile(r'^/media/.*$'),
        ]
        
        # URLs that require authentication and phone verification
        self.auth_required_urls = [
            re.compile(r'^/profile/.*$'),
            re.compile(r'^/orders/.*$'),
            re.compile(r'^/booking/.*$'),
            re.compile(r'^/checkout/.*$'),
            re.compile(r'^/payment/.*$'),
        ]
    
    def __call__(self, request):
        # Skip middleware if OTP verification is disabled
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return self.get_response(request)
        
        path = request.path_info.lstrip('/')
        
        # Check if the URL is exempt from phone verification
        if any(m.match(request.path_info) for m in self.exempt_urls):
            return self.get_response(request)
        
        # Check if the URL requires authentication and phone verification
        if any(m.match(request.path_info) for m in self.auth_required_urls):
            # Skip if OTP is already verified
            if request.session.get('otp_verified'):
                return self.get_response(request)
            
            # Redirect to OTP verification with the current URL as next parameter
            messages.warning(request, 'Please verify your phone number to access this page.')
            redirect_url = f"{reverse('astrology:verify_otp')}?next={request.path_info}"
            return redirect(redirect_url)
        
        return self.get_response(request)