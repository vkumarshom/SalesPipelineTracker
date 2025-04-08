import random
import string
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpRequest
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

def get_session_id(request: HttpRequest) -> str:
    """Get or create a session ID for the cart."""
    session_key = 'cart_session_id'
    if session_key not in request.session:
        request.session[session_key] = str(uuid.uuid4())
    return request.session[session_key]

def generate_order_number() -> str:
    """Generate a unique order number."""
    timestamp = int(datetime.utcnow().timestamp())
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"AST{timestamp}{random_chars}"

def get_available_booking_slots(service_duration: int, date, booked_slots=None, start_time=None, end_time=None) -> list:
    """
    Generate available time slots for a given date, accounting for service duration and already booked slots.
    
    Args:
        service_duration (int): Duration of the service in minutes
        date (datetime.date): The date to get slots for
        booked_slots (list): List of already booked slots as (start_time, end_time) tuples
        start_time (datetime.time, optional): Custom start time for availability
        end_time (datetime.time, optional): Custom end time for availability
        
    Returns:
        list: List of available time slots as strings in 'HH:MM' format
    """
    if booked_slots is None:
        booked_slots = []
    
    # Default business hours if not provided: 9 AM to 5 PM
    if start_time is None:
        start_time = datetime.min.time().replace(hour=9)
    
    if end_time is None:
        end_time = datetime.min.time().replace(hour=17)
    
    # Create time slots
    slot_interval = 30  # minutes - always divide slots into 30-minute intervals
    all_slots = []
    
    current_datetime = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)
    
    while current_datetime < end_datetime:
        slot_end_datetime = current_datetime + timedelta(minutes=service_duration)
        
        # Skip if there's not enough time remaining for the full service duration
        if slot_end_datetime > end_datetime:
            break
        
        # Check if slot overlaps with any booked slot
        is_available = True
        for booked_start, booked_end in booked_slots:
            booked_start_datetime = datetime.combine(date, booked_start)
            booked_end_datetime = datetime.combine(date, booked_end)
            
            if (current_datetime < booked_end_datetime and 
                slot_end_datetime > booked_start_datetime):
                is_available = False
                break
        
        if is_available:
            # Only add the slot if it's available
            all_slots.append(current_datetime.strftime('%H:%M'))
        
        # Always increment by the slot interval (30 minutes)
        current_datetime += timedelta(minutes=slot_interval)
    
    return all_slots

def format_price(amount: float) -> str:
    """Format price with two decimal places and sterling sign."""
    return f"£{amount:.2f}"

def get_cart_total(cart_items) -> float:
    """Calculate the total price of all items in the cart."""
    return sum(item.service.price * item.quantity for item in cart_items)


def send_email_notification(subject: str, message: str, recipient_list: list, html_message: str = None, fail_silently: bool = False) -> bool:
    """
    Send an email using SendGrid.
    
    Args:
        subject (str): Email subject
        message (str): Plain text email content
        recipient_list (list): List of recipient email addresses
        html_message (str, optional): HTML version of the email content
        fail_silently (bool, optional): Whether to suppress exceptions if sending fails
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        # Using Django's send_mail which will use the SendGrid backend
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=fail_silently
        )
        logger.info(f"Email sent successfully to {', '.join(recipient_list)}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        if not fail_silently:
            raise
        return False