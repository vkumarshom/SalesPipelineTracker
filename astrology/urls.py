from django.urls import path
from . import views

app_name = 'astrology'

urlpatterns = [
    # Main Pages
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Services
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # E-commerce
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('checkout/', views.checkout, name='checkout'),
    
    # Payment
    path('stripe-checkout/', views.stripe_checkout, name='stripe_checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe-success/', views.stripe_success, name='stripe_success'),
    path('stripe-cancel/', views.stripe_cancel, name='stripe_cancel'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('paypal-checkout/', views.paypal_checkout, name='paypal_checkout'),
    path('paypal-success/', views.paypal_success, name='paypal_success'),
    path('paypal-cancel/', views.paypal_cancel, name='paypal_cancel'),
    
    # Booking
    path('booking/', views.booking, name='booking'),
    path('booking/get-time-slots/', views.get_available_time_slots, name='get_time_slots'),
    path('booking/confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    
    # User Profile
    path('profile/', views.profile, name='profile'),
    path('profile/readings/', views.user_readings, name='user_readings'),
    path('profile/consultation-reports/', views.consultation_reports, name='consultation_reports'),
    path('profile/orders/', views.order_list, name='order_list'),
    path('profile/orders/<str:order_number>/', views.order_detail, name='order_detail'),
    
    # Admin Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/services/', views.admin_services, name='admin_services'),
    path('admin/services/create/', views.admin_service_create, name='admin_service_create'),
    path('admin/services/edit/<int:service_id>/', views.admin_service_edit, name='admin_service_edit'),
    path('admin/services/delete/<int:service_id>/', views.admin_service_delete, name='admin_service_delete'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/reports/create/', views.admin_report_create, name='admin_report_create'),
    path('admin/reports/edit/<int:report_id>/', views.admin_report_edit, name='admin_report_edit'),
    path('admin/reports/delete/<int:report_id>/', views.admin_report_delete, name='admin_report_delete'),
    
    # OTP Verification
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    
    # Email Testing (Admin only)
    path('admin/test-email/', views.test_email, name='test_email'),
    
    # API Endpoints
    path('api/whatsapp-config/', views.get_whatsapp_config, name='get_whatsapp_config'),
]