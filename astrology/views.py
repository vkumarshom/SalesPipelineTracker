from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import uuid
import datetime

from .models import (
    BlogPost, 
    Service, 
    Booking, 
    CartItem, 
    Order, 
    OrderItem, 
    Contact,
    UserReading
)

def index(request):
    """Homepage view"""
    services = Service.objects.filter(is_available=True)[:3]
    blog_posts = BlogPost.objects.filter(published=True)[:3]
    
    context = {
        'services': services,
        'blog_posts': blog_posts,
    }
    
    return render(request, 'astrology/index.html', context)

def about(request):
    """About page view"""
    return render(request, 'astrology/about.html')

def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and message:
            Contact.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('astrology:contact')
        else:
            messages.error(request, 'Please fill in all required fields!')
    
    return render(request, 'astrology/contact.html')

def blog_list(request):
    """Blog listing page view"""
    blog_posts_list = BlogPost.objects.filter(published=True)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        blog_posts_list = blog_posts_list.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(summary__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(blog_posts_list, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    
    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        blog_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        blog_posts = paginator.page(paginator.num_pages)
    
    context = {
        'blog_posts': blog_posts,
        'query': query,
    }
    
    return render(request, 'astrology/blog/index.html', context)

def blog_detail(request, slug):
    """Blog post detail view"""
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    recent_posts = BlogPost.objects.filter(published=True).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    
    return render(request, 'astrology/blog/post.html', context)

def service_list(request):
    """Services listing page view"""
    services = Service.objects.filter(is_available=True)
    
    context = {
        'services': services,
    }
    
    return render(request, 'astrology/services.html', context)

def service_detail(request, slug):
    """Service detail view"""
    service = get_object_or_404(Service, slug=slug, is_available=True)
    related_services = Service.objects.filter(is_available=True).exclude(id=service.id)[:3]
    
    context = {
        'service': service,
        'related_services': related_services,
    }
    
    return render(request, 'astrology/shop/product.html', context)

def get_session_id(request):
    """Get or create a session ID for the cart"""
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def cart(request):
    """Shopping cart view"""
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    total = sum(item.service.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'astrology/shop/cart.html', context)

@require_POST
def add_to_cart(request):
    """Add item to cart AJAX view"""
    service_id = request.POST.get('service_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if service_id:
        session_id = get_session_id(request)
        service = get_object_or_404(Service, id=service_id, is_available=True)
        
        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            service=service,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Return JSON response
        return JsonResponse({
            'status': 'success',
            'message': f'{service.name} added to cart',
            'cart_count': CartItem.objects.filter(session_id=session_id).count()
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@require_POST
def update_cart(request):
    """Update cart item quantity AJAX view"""
    item_id = request.POST.get('item_id')
    quantity = int(request.POST.get('quantity', 1))
    
    if item_id and quantity > 0:
        session_id = get_session_id(request)
        cart_item = get_object_or_404(CartItem, id=item_id, session_id=session_id)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        # Calculate new totals
        cart_items = CartItem.objects.filter(session_id=session_id)
        item_total = cart_item.service.price * quantity
        cart_total = sum(item.service.price * item.quantity for item in cart_items)
        
        return JsonResponse({
            'status': 'success',
            'item_total': item_total,
            'cart_total': cart_total
        })
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def remove_from_cart(request, item_id):
    """Remove item from cart"""
    session_id = get_session_id(request)
    cart_item = get_object_or_404(CartItem, id=item_id, session_id=session_id)
    cart_item.delete()
    
    messages.success(request, 'Item removed from cart')
    return redirect('astrology:cart')

def checkout(request):
    """Checkout page view"""
    session_id = get_session_id(request)
    cart_items = CartItem.objects.filter(session_id=session_id)
    
    if not cart_items:
        messages.error(request, 'Your cart is empty')
        return redirect('astrology:cart')
    
    total = sum(item.service.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone', '')
        
        if customer_name and customer_email:
            # Create order
            order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
            
            order = Order.objects.create(
                order_number=order_number,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                total_amount=total,
                status='pending',
                user=request.user if request.user.is_authenticated else None
            )
            
            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    service=item.service,
                    service_name=item.service.name,
                    price=item.service.price,
                    quantity=item.quantity
                )
            
            # Clear cart
            cart_items.delete()
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('astrology:index')
        else:
            messages.error(request, 'Please fill in all required fields!')
    
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'astrology/shop/checkout.html', context)

def booking(request):
    """Booking page view"""
    services = Service.objects.filter(is_available=True)
    
    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone', '')
        notes = request.POST.get('notes', '')
        
        if service_id and booking_date and booking_time and customer_name and customer_email:
            service = get_object_or_404(Service, id=service_id, is_available=True)
            
            # Convert date and time strings to proper types
            booking_date = datetime.datetime.strptime(booking_date, '%Y-%m-%d').date()
            booking_time = datetime.datetime.strptime(booking_time, '%H:%M').time()
            
            # Create booking
            booking = Booking.objects.create(
                service=service,
                customer_name=customer_name,
                customer_email=customer_email,
                customer_phone=customer_phone,
                booking_date=booking_date,
                booking_time=booking_time,
                notes=notes,
                status='pending',
                user=request.user if request.user.is_authenticated else None
            )
            
            messages.success(request, 'Your booking has been submitted successfully!')
            return redirect('astrology:booking_confirmation', booking_id=booking.id)
        else:
            messages.error(request, 'Please fill in all required fields!')
    
    context = {
        'services': services,
    }
    
    return render(request, 'astrology/booking/calendar.html', context)

def booking_confirmation(request, booking_id):
    """Booking confirmation page view"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'astrology/booking/confirmation.html', context)

@login_required
def profile(request):
    """User profile page"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'bookings': bookings,
        'orders': orders,
    }
    
    return render(request, 'astrology/profile.html', context)

@login_required
def user_readings(request):
    """User readings page"""
    readings = UserReading.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'readings': readings,
    }
    
    return render(request, 'astrology/readings.html', context)