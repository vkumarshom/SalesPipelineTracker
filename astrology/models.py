import os
import random
import string
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from datetime import timedelta

class Profile(models.Model):
    """
    Extended user profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_time = models.TimeField(blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create Profile when User is created"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save Profile when User is saved"""
    instance.profile.save()

class OTP(models.Model):
    """
    OTP model for phone verification
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"OTP for {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # Set expiry to 5 minutes from creation
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

class Service(models.Model):
    """
    Astrology consultation service model
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at field removed temporarily until migration is created
    # updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('astrology:service_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class AvailabilitySlot(models.Model):
    """
    Model for defining available time slots for bookings
    """
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    day_of_week = models.IntegerField(choices=DAY_CHOICES, help_text="Day of week (0=Monday, 6=Sunday)")
    start_time = models.TimeField(help_text="Start time for availability (e.g., 09:00)")
    end_time = models.TimeField(help_text="End time for availability (e.g., 17:00)")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        verbose_name = "Availability Slot"
        verbose_name_plural = "Availability Slots"

class BlockedDate(models.Model):
    """
    Model for blocked dates when no bookings are allowed
    """
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"Blocked: {self.date.strftime('%Y-%m-%d')}"
    
    class Meta:
        ordering = ['date']
        verbose_name = "Blocked Date"
        verbose_name_plural = "Blocked Dates"

class Booking(models.Model):
    """
    Booking model for astrology consultations
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    booking_time = models.TimeField()
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = PhoneNumberField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_guest_booking = models.BooleanField(default=False, help_text="Whether this booking was made by a guest (non-registered user)")
    registration_link_sent = models.BooleanField(default=False, help_text="Whether a registration link has been sent to this guest user")
    
    def __str__(self):
        return f"{self.customer_name} - {self.service.name} on {self.booking_date} at {self.booking_time}"
    
    class Meta:
        ordering = ['-booking_date', '-booking_time']

class BlogPost(models.Model):
    """
    Blog post model
    """
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    summary = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('astrology:blog_detail', args=[self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['-created_at']

class Coupon(models.Model):
    """
    Coupon code model for discounts
    """
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True, help_text="Percentage discount (0-100)")
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Fixed amount discount")
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField()
    min_purchase_amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.code
    
    @property
    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_to and
            (self.max_uses is None or self.used_count < self.max_uses)
        )

class CartItem(models.Model):
    """
    Shopping cart item model
    """
    session_id = models.CharField(max_length=64)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity} x {self.service.name}"
    
    @property
    def total_price(self):
        return self.quantity * self.service.price

class Order(models.Model):
    """
    Order model
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_CHOICES = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('other', 'Other'),
    )
    
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = PhoneNumberField(blank=True, null=True)
    subtotal_amount = models.DecimalField(max_digits=8, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='stripe')
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.order_number
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    """
    Order item model
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.service_name}"
    
    @property
    def total_price(self):
        return self.quantity * self.price

class Contact(models.Model):
    """
    Contact form submission model
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']

class UserReading(models.Model):
    """
    User astrology reading model
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='readings')
    title = models.CharField(max_length=100)
    content = models.TextField()
    reading_date = models.DateField(default=timezone.now)
    is_public = models.BooleanField(default=False)
    pdf_report = models.FileField(upload_to='reports/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']
        
    def get_pdf_filename(self):
        if self.pdf_report:
            return os.path.basename(self.pdf_report.name)
        return None
        
class ConsultationReport(models.Model):
    """
    Consultation reports model for PDF uploads
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_reports')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    report_file = models.FileField(upload_to='consultation_reports/')
    consultation_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']
        
    def get_filename(self):
        return os.path.basename(self.report_file.name)
        
class WhatsAppConfig(models.Model):
    """
    WhatsApp configuration for chat integration
    """
    phone_number = PhoneNumberField(help_text="WhatsApp phone number with country code (e.g., +447123456789)")
    default_message = models.CharField(max_length=255, default="Hello, I'd like to book an astrology consultation.", 
                                     help_text="Default message that will be pre-filled when users click to contact via WhatsApp")
    display_name = models.CharField(max_length=100, default="MetaMystic Astrology",
                                  help_text="Name to display in the chat widget")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"WhatsApp Config: {self.phone_number}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active configuration exists
        if self.is_active:
            WhatsAppConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active(cls):
        """Get the active WhatsApp configuration"""
        try:
            return cls.objects.filter(is_active=True).first()
        except cls.DoesNotExist:
            return None
    
    class Meta:
        verbose_name = "WhatsApp Configuration"
        verbose_name_plural = "WhatsApp Configurations"