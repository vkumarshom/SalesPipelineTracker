from django.contrib import admin
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

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published', 'created_at')
    list_filter = ('published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_available')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'service', 'booking_date', 'booking_time', 'status')
    list_filter = ('status', 'booking_date')
    search_fields = ('customer_name', 'customer_email')
    ordering = ('-booking_date', '-booking_time')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'service', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('session_id',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email')
    ordering = ('-created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'service_name', 'price', 'quantity')
    search_fields = ('service_name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)

@admin.register(UserReading)
class UserReadingAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    ordering = ('-created_at',)