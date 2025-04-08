import random
import string
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from django.http import HttpRequest

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

def get_available_booking_slots(service_duration: int, date, booked_slots=None) -> list:
    """
    Generate available time slots for a given date, accounting for service duration and already booked slots.
    
    Args:
        service_duration (int): Duration of the service in minutes
        date (datetime.date): The date to get slots for
        booked_slots (list): List of already booked slots as (start_time, end_time) tuples
        
    Returns:
        list: List of available time slots as strings in 'HH:MM' format
    """
    if booked_slots is None:
        booked_slots = []
    
    # Business hours: 9 AM to 5 PM
    start_hour = 9
    end_hour = 17
    
    # Create time slots
    slot_interval = 30  # minutes
    all_slots = []
    
    current_time = datetime.combine(date, datetime.min.time().replace(hour=start_hour))
    end_time = datetime.combine(date, datetime.min.time().replace(hour=end_hour))
    
    while current_time < end_time:
        slot_end = current_time + timedelta(minutes=service_duration)
        
        # Check if slot overlaps with any booked slot
        is_available = True
        for booked_start, booked_end in booked_slots:
            if (current_time < booked_end and slot_end > booked_start):
                is_available = False
                break
        
        if is_available and slot_end <= end_time:
            all_slots.append(current_time.strftime('%H:%M'))
        
        current_time += timedelta(minutes=slot_interval)
    
    return all_slots

def format_price(amount: float) -> str:
    """Format price with two decimal places and sterling sign."""
    return f"£{amount:.2f}"

def get_cart_total(cart_items) -> float:
    """Calculate the total price of all items in the cart."""
    return sum(item.service.price * item.quantity for item in cart_items)