from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages, auth
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
import string
import uuid
import json
import requests
import os
from decimal import Decimal
from datetime import datetime, timedelta

from .models import (
    Profile, OTP, Service, Booking, BlogPost, CartItem, 
    Order, OrderItem, Contact, Coupon, UserReading,
    AvailabilitySlot, BlockedDate, ConsultationReport
)
from .forms import (
    OTPVerificationForm, ContactForm, BookingForm, CouponForm,
    CustomRegisterForm, CustomLoginForm, ConsultationReportForm,
    UserReadingForm
)
from .utils import (
    get_session_id, generate_order_number, get_available_booking_slots,
    format_price, get_cart_total, send_email_notification
)

# OTP Generation and Verification
def generate_otp():
    """Generate a 6-digit OTP code"""
    return ''.join(random.choices(string.digits, k=6))

def send_otp(user, otp_code):
    """
    Send OTP code via SMS
    This is a placeholder - in production, integrate with an SMS service API like Twilio
    """
    phone_number = user.profile.phone_number
    print(f"Sending OTP {otp_code} to {phone_number}")
    # In production, implement actual SMS sending logic
    return True

@login_required
def verify_otp(request):
    """View for OTP verification"""
    next_url = request.GET.get('next', reverse('astrology:profile'))
    
    # If already verified, redirect
    if request.session.get('otp_verified'):
        return redirect(next_url)
    
    # Check if user has a pending OTP
    latest_otp = OTP.objects.filter(
        user=request.user,
        is_used=False,
        expires_at__gt=timezone.now()
    ).order_by('-created_at').first()
    
    # If no valid OTP exists, create one
    if not latest_otp:
        otp_code = generate_otp()
        latest_otp = OTP.objects.create(
            user=request.user,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=5)
        )
        send_otp(request.user, otp_code)
        messages.info(request, "A new verification code has been sent to your phone.")
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp_code']
            
            # Verify OTP
            if latest_otp and latest_otp.otp_code == entered_otp:
                if latest_otp.is_expired:
                    messages.error(request, "Verification code has expired. Please request a new one.")
                else:
                    # Mark OTP as used
                    latest_otp.is_used = True
                    latest_otp.save()
                    
                    # Mark phone as verified
                    profile = request.user.profile
                    profile.is_phone_verified = True
                    profile.save()
                    
                    # Set session flag
                    request.session['otp_verified'] = True
                    
                    messages.success(request, "Phone number verified successfully!")
                    return redirect(next_url)
            else:
                messages.error(request, "Invalid verification code. Please try again.")
    else:
        form = OTPVerificationForm()
    
    return render(request, 'astrology/verify_otp.html', {'form': form})

@login_required
def resend_otp(request):
    """Resend OTP code"""
    # Invalidate existing OTPs
    OTP.objects.filter(user=request.user, is_used=False).update(is_used=True)
    
    # Generate and send new OTP
    otp_code = generate_otp()
    OTP.objects.create(
        user=request.user,
        otp_code=otp_code,
        expires_at=timezone.now() + timedelta(minutes=5)
    )
    send_otp(request.user, otp_code)
    
    messages.success(request, "A new verification code has been sent to your phone.")
    
    # Redirect back to verify OTP page
    next_url = request.GET.get('next', '')
    if next_url:
        return redirect(f"{reverse('astrology:verify_otp')}?next={next_url}")
    else:
        return redirect('astrology:verify_otp')

# Main Views
def index(request):
    """Homepage view"""
    services = Service.objects.filter(is_available=True)[:3]
    recent_posts = BlogPost.objects.filter(published=True)[:3]
    return render(request, 'astrology/index.html', {
        'services': services,
        'recent_posts': recent_posts
    })

def about(request):
    """About page view"""
    return render(request, 'astrology/about.html')

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            messages.success(request, "Your message has been sent. We'll get back to you soon!")
            return redirect('astrology:contact')
    else:
        form = ContactForm()
    
    return render(request, 'astrology/contact.html', {'form': form})

def services(request):
    """Services listing page view"""
    services_list = Service.objects.filter(is_available=True)
    return render(request, 'astrology/services.html', {'services': services_list})

def service_detail(request, slug):
    """Service detail view"""
    service = get_object_or_404(Service, slug=slug, is_available=True)
    return render(request, 'astrology/service_detail.html', {'service': service})

def blog_list(request):
    """Blog listing page view"""
    posts_list = BlogPost.objects.filter(published=True)
    paginator = Paginator(posts_list, 6)  # 6 posts per page
    
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'blog/index.html', {'posts': posts})

def blog_detail(request, slug):
    """Blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    recent_posts = BlogPost.objects.filter(published=True).exclude(id=post.id)[:3]
    
    return render(request, 'blog/post.html', {
        'post': post,
        'recent_posts': recent_posts
    })

# E-commerce Views

def cart(request):
    """Shopping cart view"""
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    # Calculate totals
    subtotal = sum(item.service.price * item.quantity for item in cart_items)
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total': subtotal
    })

@require_POST
def add_to_cart(request):
    """Add item to cart AJAX view"""
    service_id = request.POST.get('service_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not service_id:
        return JsonResponse({'error': 'Service ID is required'}, status=400)
    
    try:
        service = Service.objects.get(id=service_id, is_available=True)
    except Service.DoesNotExist:
        return JsonResponse({'error': 'Service not found'}, status=404)
    
    session_id = get_session_id(request)
    
    # Check if item already in cart
    cart_item, created = CartItem.objects.get_or_create(
        session_id=session_id,
        service=service,
        defaults={'quantity': quantity}
    )
    
    # If item exists, update quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    # Get updated cart count
    cart_count = CartItem.objects.filter(session_id=session_id).aggregate(
        total=Sum('quantity')
    )['total'] or 0
    
    return JsonResponse({
        'success': True,
        'message': f'{service.name} added to cart',
        'cart_count': cart_count
    })

@require_POST
def update_cart(request):
    """Update cart item quantity AJAX view"""
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if not item_id:
        return JsonResponse({'error': 'Item ID is required'}, status=400)
    
    try:
        cart_item = CartItem.objects.get(id=item_id, session_id=get_session_id(request))
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'Cart item not found'}, status=404)
    
    if quantity <= 0:
        cart_item.delete()
        return JsonResponse({'success': True, 'removed': True})
    else:
        cart_item.quantity = quantity
        cart_item.save()
    
    # Recalculate cart totals
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    subtotal = sum(item.service.price * item.quantity for item in cart_items)
    
    return JsonResponse({
        'success': True,
        'item_total': float(cart_item.service.price * cart_item.quantity),
        'subtotal': float(subtotal),
        'total': float(subtotal),  # Add tax/shipping if needed
    })

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart_item = CartItem.objects.get(id=item_id, session_id=get_session_id(request))
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in cart.")
    
    return redirect('astrology:cart')

@require_POST
def apply_coupon(request):
    """Apply coupon code to cart"""
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                is_active=True,
                valid_from__lte=timezone.now(),
                valid_to__gte=timezone.now()
            )
            
            # Check if maximum uses reached
            if coupon.max_uses and coupon.used_count >= coupon.max_uses:
                messages.error(request, "This coupon has reached its maximum number of uses.")
                return redirect('astrology:cart')
            
            # Calculate cart total to check minimum purchase
            session_id = get_session_id(request)
            cart_items = CartItem.objects.filter(session_id=session_id)
            subtotal = sum(item.service.price * item.quantity for item in cart_items)
            
            if coupon.min_purchase_amount and subtotal < coupon.min_purchase_amount:
                messages.error(
                    request, 
                    f"This coupon requires a minimum purchase of £{coupon.min_purchase_amount}."
                )
                return redirect('astrology:cart')
            
            # Store coupon in session
            request.session['coupon_id'] = coupon.id
            messages.success(request, f"Coupon '{coupon.code}' applied successfully.")
            
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code or expired.")
    
    return redirect('astrology:cart')

def checkout(request):
    """Checkout page view"""
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('astrology:cart')
    
    # Calculate totals
    subtotal = sum(item.service.price * item.quantity for item in cart_items)
    discount = Decimal('0.00')
    
    # Apply coupon if exists
    coupon = None
    coupon_id = None
    if request.session.get('coupon_id'):
        try:
            coupon = Coupon.objects.get(id=request.session['coupon_id'])
            coupon_id = coupon.id
            if coupon.discount_percentage:
                discount = subtotal * (coupon.discount_percentage / Decimal('100.0'))
            elif coupon.discount_amount:
                discount = min(coupon.discount_amount, subtotal)  # Don't exceed cart total
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
    
    total = subtotal - discount
    
    # Store order details in session for later use
    order_number = generate_order_number()
    order_details = {
        'order_number': order_number,
        'subtotal': float(subtotal),
        'discount': float(discount),
        'total': float(total),
        'coupon_id': coupon_id
    }
    request.session['order_details'] = order_details
    
    return render(request, 'shop/checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'coupon': coupon,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'order_number': order_number
    })

@require_POST
def create_checkout_session(request):
    """Create Stripe checkout session and redirect user to Stripe's hosted checkout page"""
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    order_details = request.session.get('order_details', {})
    if not order_details:
        messages.error(request, "Invalid order information.")
        return redirect('astrology:checkout')
    
    order_number = order_details.get('order_number')
    total_amount = order_details.get('total', 0)
    
    # Get cart items to create line items
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    # Format items for Stripe
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': item.service.name,
                    'description': item.service.short_description,
                },
                'unit_amount': int(item.service.price * 100),  # Stripe needs amount in pennies
            },
            'quantity': item.quantity,
        })
    
    # Set domain based on environment
    domain_url = f"https://{settings.REPLIT_DEV_DOMAIN}"
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=domain_url + reverse('astrology:stripe_success') + f'?order_number={order_number}',
            cancel_url=domain_url + reverse('astrology:stripe_cancel'),
            metadata={
                'order_number': order_number,
            }
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f"Error creating checkout session: {str(e)}")
        return redirect('astrology:checkout')

# Booking Views
def booking(request):
    """Booking page view"""
    services = Service.objects.filter(is_available=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, services=services)
        if form.is_valid():
            service = Service.objects.get(id=form.cleaned_data['service'])
            booking = Booking(
                service=service,
                booking_date=form.cleaned_data['date'],
                booking_time=form.cleaned_data['time'],
                customer_name=form.cleaned_data['name'],
                customer_email=form.cleaned_data['email'],
                customer_phone=form.cleaned_data['phone'],
                notes=form.cleaned_data['notes']
            )
            
            # Handle guest or logged-in user booking
            if request.user.is_authenticated:
                booking.user = request.user
                booking.is_guest_booking = False
            else:
                booking.is_guest_booking = True
                
                # Create a new user account if requested
                if form.cleaned_data.get('create_account'):
                    try:
                        # Generate a random username if needed
                        username = form.cleaned_data['email'].split('@')[0]
                        if User.objects.filter(username=username).exists():
                            username = f"{username}_{random.randint(1000, 9999)}"
                            
                        # Generate a random password
                        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                        
                        # Create the user
                        user = User.objects.create_user(
                            username=username,
                            email=form.cleaned_data['email'],
                            password=temp_password,
                            first_name=form.cleaned_data['name'].split(' ')[0],
                            last_name=' '.join(form.cleaned_data['name'].split(' ')[1:]) if len(form.cleaned_data['name'].split(' ')) > 1 else ''
                        )
                        
                        # Link the booking to the new user
                        booking.user = user
                        booking.is_guest_booking = False
                        
                        # Send welcome email with login details
                        # TODO: Implement email sending with the temp password
                        
                    except Exception as e:
                        # Log the error but continue with guest booking
                        print(f"Error creating user account: {str(e)}")
            
            booking.save()
            
            return redirect('astrology:booking_confirmation', booking_id=booking.id)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
                'phone': request.user.profile.phone_number if hasattr(request.user, 'profile') else None
            }
        form = BookingForm(services=services, initial=initial)
    
    return render(request, 'booking/calendar.html', {'form': form, 'services': services})

@require_GET
def get_available_time_slots(request):
    """Get available time slots for a specific date and service"""
    date_str = request.GET.get('date')
    service_id = request.GET.get('service_id')
    
    if not date_str or not service_id:
        return JsonResponse({'error': 'Date and service ID are required'}, status=400)
    
    try:
        # Parse date
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if date is blocked
        if BlockedDate.objects.filter(date=date).exists():
            return JsonResponse({'slots': []})
        
        # Get the service for duration
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return JsonResponse({'error': 'Service not found'}, status=404)
        
        # Get all existing bookings for this date to check for conflicts
        existing_bookings = Booking.objects.filter(
            booking_date=date, 
            status__in=['pending', 'confirmed']
        ).values_list('booking_time', 'service__duration')
        
        # Convert to list of (start_time, end_time) tuples for conflict checking
        booked_slots = []
        for booking_time, duration in existing_bookings:
            start = timezone.datetime.combine(date, booking_time)
            end = start + timezone.timedelta(minutes=duration)
            booked_slots.append((booking_time, end.time()))
        
        # Get day of week (0=Monday, 6=Sunday)
        day_of_week = date.weekday()
        
        # Get availability slots for this day
        availability = AvailabilitySlot.objects.filter(
            day_of_week=day_of_week,
            is_active=True
        )
        
        # If no specific availability set for this day, use default business hours (9 AM - 5 PM)
        if not availability.exists():
            today = timezone.datetime.today().date()
            
            # Only show future slots if booking for today
            if date == today:
                current_time = timezone.now().time()
                start_time = max(timezone.datetime.strptime('09:00', '%H:%M').time(), current_time)
            else:
                start_time = timezone.datetime.strptime('09:00', '%H:%M').time()
                
            end_time = timezone.datetime.strptime('17:00', '%H:%M').time()
            available_times = get_available_booking_slots(service.duration, date, booked_slots)
        else:
            # Generate slots for each availability period
            available_times = []
            for slot in availability:
                # For today, don't show past slots
                if date == timezone.datetime.today().date() and timezone.now().time() > slot.start_time:
                    start_time = timezone.now().time()
                else:
                    start_time = slot.start_time
                
                # Get slots for this availability period
                period_slots = get_available_booking_slots(
                    service.duration, 
                    date, 
                    booked_slots,
                    start_time=start_time,
                    end_time=slot.end_time
                )
                available_times.extend(period_slots)
        
        return JsonResponse({'slots': available_times})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def booking_confirmation(request, booking_id):
    """Booking confirmation page view"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: only allow viewing if user owns the booking or booking email matches session
    if (request.user.is_authenticated and booking.user == request.user) or \
       (request.session.get('booking_email') == booking.customer_email):
        return render(request, 'booking/confirmation.html', {'booking': booking})
    else:
        # Store email in session for security verification
        request.session['booking_email'] = booking.customer_email
        return render(request, 'booking/confirmation.html', {'booking': booking})

# User Profile Views
@login_required
def profile(request):
    """User profile page"""
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-booking_date', '-booking_time')
    orders = Order.objects.filter(user=user).order_by('-created_at')
    readings = UserReading.objects.filter(user=user).order_by('-created_at')
    
    return render(request, 'astrology/profile.html', {
        'user': user,
        'bookings': bookings,
        'orders': orders,
        'readings': readings
    })

@login_required
def user_readings(request):
    """User readings page"""
    readings = UserReading.objects.filter(user=request.user).order_by('-created_at')
    consultation_reports = ConsultationReport.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'astrology/readings.html', {
        'readings': readings,
        'consultation_reports': consultation_reports
    })
    
@login_required
def consultation_reports(request):
    """User consultation reports page"""
    reports = ConsultationReport.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'astrology/consultation_reports.html', {'reports': reports})

@login_required
def order_list(request):
    """User orders list view"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'astrology/orders.html', {'orders': orders})

@login_required
def order_detail(request, order_number):
    """Order detail view"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'astrology/order_detail.html', {'order': order})

# Payment Views
def stripe_checkout(request):
    """Redirect to Stripe Checkout"""
    if not settings.STRIPE_SECRET_KEY:
        messages.error(request, "Payment processing is currently unavailable.")
        return redirect('astrology:checkout')
    
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('astrology:cart')
    
    # Calculate totals
    subtotal = sum(item.service.price * item.quantity for item in cart_items)
    discount = Decimal('0.00')
    
    # Apply coupon if exists
    coupon = None
    if request.session.get('coupon_id'):
        try:
            coupon = Coupon.objects.get(id=request.session['coupon_id'])
            if coupon.discount_percentage:
                discount = subtotal * (coupon.discount_percentage / Decimal('100.0'))
            elif coupon.discount_amount:
                discount = min(coupon.discount_amount, subtotal)
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
    
    total = subtotal - discount
    
    # Create Stripe line items
    line_items = []
    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': item.service.name,
                    'description': item.service.short_description,
                },
                'unit_amount': int(item.service.price * 100),  # Stripe uses cents
            },
            'quantity': item.quantity,
        })
    
    # Generate unique order number
    order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    
    # Create Stripe checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(
                reverse('astrology:stripe_success')
            ) + f"?order_number={order_number}",
            cancel_url=request.build_absolute_uri(reverse('astrology:stripe_cancel')),
            metadata={
                'order_number': order_number,
                'coupon_id': str(coupon.id) if coupon else '',
            }
        )
        
        # Store order details in session for retrieval on success
        request.session['order_details'] = {
            'order_number': order_number,
            'subtotal': float(subtotal),
            'discount': float(discount),
            'total': float(total),
            'coupon_id': coupon.id if coupon else None,
        }
        
        return redirect(checkout_session.url)
    
    except Exception as e:
        messages.error(request, f"Error creating checkout session: {str(e)}")
        return redirect('astrology:checkout')

def stripe_success(request):
    """Stripe payment success view"""
    order_number = request.GET.get('order_number')
    order_details = request.session.get('order_details', {})
    
    if not order_number or not order_details:
        messages.error(request, "Invalid order information.")
        return redirect('astrology:checkout')
    
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    # Create the order
    order = Order(
        order_number=order_number,
        user=request.user if request.user.is_authenticated else None,
        customer_name=request.POST.get('customer_name', 'Guest'),
        customer_email=request.POST.get('customer_email', 'guest@example.com'),
        customer_phone=request.POST.get('customer_phone', ''),
        subtotal_amount=Decimal(str(order_details.get('subtotal', 0))),
        discount_amount=Decimal(str(order_details.get('discount', 0))),
        total_amount=Decimal(str(order_details.get('total', 0))),
        payment_method='stripe',
        status='paid'
    )
    
    # Set coupon if used
    coupon_id = order_details.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            order.coupon = coupon
            # Update coupon usage count
            coupon.used_count += 1
            coupon.save()
        except Coupon.DoesNotExist:
            pass
    
    order.save()
    
    # Create order items
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            service=item.service,
            service_name=item.service.name,
            price=item.service.price,
            quantity=item.quantity
        )
    
    # Clear cart and session data
    cart_items.delete()
    request.session.pop('order_details', None)
    request.session.pop('coupon_id', None)
    
    # Return payment success page with order details
    return render(request, "shop/payment_success.html", {"order": order})


def stripe_cancel(request):
    """Stripe payment cancel view"""
    return render(request, "shop/payment_cancel.html")


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None

    try:
        if endpoint_secret:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        else:
            # Without the webhook secret we can't validate the signature,
            # but we can still parse the event for testing
            event = json.loads(payload)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        # Invalid payload or signature
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Retrieve the metadata from the session
        order_number = session.get('metadata', {}).get('order_number')
        if order_number:
            # Find the order or create it if it doesn't exist
            try:
                order = Order.objects.get(order_number=order_number)
                order.payment_id = session.get('payment_intent')
                order.status = 'paid'
                order.save()
                
                # Empty the cart associated with the order
                try:
                    cart_items = CartItem.objects.filter(session_id=session.get('client_reference_id'))
                    cart_items.delete()
                except Exception as e:
                    # Log the error but continue
                    print(f"Error clearing cart: {str(e)}")
            except Order.DoesNotExist:
                # Order doesn't exist - log this as an error
                print(f"Order {order_number} not found for webhook event")
    
    return HttpResponse(status=200)

def paypal_checkout(request):
    """Redirect to PayPal Checkout"""
    messages.info(request, "PayPal checkout flow will be implemented here.")
    return redirect('astrology:checkout')

def paypal_success(request):
    """PayPal payment success view"""
    messages.success(request, "PayPal payment successful!")
    return redirect('astrology:checkout')

def paypal_cancel(request):
    """PayPal payment cancel view"""
    messages.warning(request, "PayPal payment was cancelled.")
    return redirect('astrology:checkout')

# Authentication Views
def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('astrology:profile')
        
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            
            # Create profile with phone number
            profile = Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number']
            )
            
            # Generate and send OTP
            otp_code = generate_otp()
            OTP.objects.create(
                user=user,
                otp_code=otp_code,
                expires_at=timezone.now() + timedelta(minutes=5)
            )
            
            # Log the user in
            user = authenticate(request, username=form.cleaned_data['username'], 
                              password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                
            # Send OTP
            send_otp(user, otp_code)
            
            messages.success(request, "Registration successful! Please verify your phone number.")
            return redirect('astrology:verify_otp')
    else:
        form = CustomRegisterForm()
    
    return render(request, 'astrology/register.html', {'form': form})

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('astrology:profile')
        
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            
            # Try to authenticate with username
            user = authenticate(username=username, password=password)
            
            # If authentication fails, try with email
            if user is None:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            
            if user is not None:
                login(request, user)
                
                # Remember me functionality
                if not remember_me:
                    request.session.set_expiry(0)  # Session expires when browser closes
                else:
                    # Session lasts for 2 weeks
                    request.session.set_expiry(60 * 60 * 24 * 14)
                
                # Check if phone verification is required
                if hasattr(user, 'profile') and not user.profile.is_phone_verified:
                    return redirect('astrology:verify_otp')
                
                # Redirect to next URL if provided
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                    
                return redirect('astrology:profile')
            else:
                messages.error(request, "Invalid username/email or password")
    else:
        form = CustomLoginForm()
    
    return render(request, 'astrology/login.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('astrology:index')

# Admin Views
@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('astrology:index')
    
    # Get statistics for dashboard
    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_bookings = Booking.objects.count()
    total_services = Service.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    recent_bookings = Booking.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_orders': total_orders,
        'total_bookings': total_bookings,
        'total_services': total_services,
        'recent_orders': recent_orders,
        'recent_bookings': recent_bookings,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
def admin_reports(request):
    """Admin consultation reports list view"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('astrology:index')
    
    reports = ConsultationReport.objects.all().order_by('-created_at')
    
    return render(request, 'admin/reports.html', {'reports': reports})

@login_required
def admin_report_create(request):
    """Admin view to create a new consultation report"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('astrology:index')
    
    if request.method == 'POST':
        form = ConsultationReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            messages.success(request, f"Report '{report.title}' created successfully.")
            return redirect('astrology:admin_reports')
    else:
        form = ConsultationReportForm()
    
    return render(request, 'admin/report_form.html', {'form': form, 'action': 'Create'})

@login_required
def admin_report_edit(request, report_id):
    """Admin view to edit a consultation report"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('astrology:index')
    
    report = get_object_or_404(ConsultationReport, id=report_id)
    
    if request.method == 'POST':
        form = ConsultationReportForm(request.POST, request.FILES, instance=report)
        if form.is_valid():
            report = form.save()
            messages.success(request, f"Report '{report.title}' updated successfully.")
            return redirect('astrology:admin_reports')
    else:
        form = ConsultationReportForm(instance=report)
    
    return render(request, 'admin/report_form.html', {'form': form, 'report': report, 'action': 'Edit'})

@login_required
def admin_report_delete(request, report_id):
    """Admin view to delete a consultation report"""
    if not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('astrology:index')
    
    report = get_object_or_404(ConsultationReport, id=report_id)
    
    if request.method == 'POST':
        report_title = report.title
        report.delete()
        messages.success(request, f"Report '{report_title}' deleted successfully.")
        return redirect('astrology:admin_reports')
    
    return render(request, 'admin/report_confirm_delete.html', {'report': report})


def test_email(request):
    """View to test email functionality with SendGrid"""
    if not request.user.is_superuser:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('astrology:index')
        
    success = False
    if request.method == 'POST':
        recipient = request.POST.get('email')
        if recipient:
            subject = "MetaMystic - Email Test"
            message = "This is a test email from MetaMystic to verify the email functionality is working correctly."
            html_message = """
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 5px;">
                <h2 style="color: #6d1b7b;">MetaMystic Email Test</h2>
                <p>Hello,</p>
                <p>This is a test email from MetaMystic to verify that the email functionality is working correctly with SendGrid.</p>
                <p>If you received this email, it means our email system is configured properly and ready to send password reset emails and other notifications.</p>
                <p style="margin-top: 30px;">Best regards,<br>The MetaMystic Team</p>
            </div>
            """
            
            success = send_email_notification(
                subject=subject,
                message=message,
                recipient_list=[recipient],
                html_message=html_message
            )
            
            if success:
                messages.success(request, f"Test email sent successfully to {recipient}!")
            else:
                messages.error(request, f"Failed to send email to {recipient}. Please check the server logs.")
        else:
            messages.error(request, "Please provide a valid email address.")
    
    return render(request, 'admin/test_email.html', {'success': success})