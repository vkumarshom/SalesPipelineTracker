# MetaMystic - Astrology Consultancy Platform

## Project Overview
MetaMystic (formerly Celestial Insights) is an astrology consultancy platform that offers immersive digital experiences and interactive celestial insights for users exploring astrological wisdom.

## Core Features
- User authentication with social login (Google, Instagram, Facebook)
- Mobile/email OTP verification
- Booking system for astrology consultation services
- E-commerce functionality with Stripe and PayPal payment processing
- Coupon code system for discounts
- Blog content management
- Consultation reports system with PDF uploads
- Interactive chat widget with WhatsApp integration
- Personal dashboard for users to access their readings/reports

## Tech Stack
- **Framework**: Django
- **Database**: PostgreSQL
- **Frontend**: HTML/CSS with Bootstrap
- **JavaScript**: For dynamic interactions
- **Payments**: Stripe and PayPal integration
- **Email**: SendGrid

## Project Structure

### Main Django Apps
- `metamystic/` - Main Django project settings and configuration
- `astrology/` - Main application with all core functionality
  - `models.py` - Database models
  - `views.py` - View controllers
  - `forms.py` - Form definitions
  - `urls.py` - URL routing
  - `utils.py` - Utility functions
  - `admin.py` - Admin interface customization
  - `migrations/` - Database migrations

### Templates & Static Files
- `templates/` - HTML templates
  - `astrology/` - App-specific templates
  - `admin/` - Admin interface templates
  - `account/` - Authentication-related templates
  - `blog/` - Blog templates
  - `booking/` - Booking system templates
- `static/` - Static assets
  - `css/` - CSS stylesheets
  - `js/` - JavaScript files
  - `assets/` - Images and other media
- `media/` - User-uploaded content
  - `profile_images/` - User profile images
  - `blog_images/` - Blog post images
  - `service_images/` - Service images

## Key Models
- `Profile` - Extended user profile with phone number and birth details
- `OTP` - One-time passwords for verification
- `Service` - Astrology consultation services offered
- `Booking` - Customer bookings for services
- `BlogPost` - Blog articles and content
- `Order` and `OrderItem` - E-commerce order management
- `ConsultationReport` - PDF reports for user consultations
- `WhatsAppConfig` - WhatsApp integration settings

## Database Schema
The database schema is available in `db_schema_django.sql` file.

## Setup Instructions
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`

## Environment Variables
The following environment variables are required:
- `DATABASE_URL` - PostgreSQL database URL
- `SENDGRID_API_KEY` - SendGrid API key for email sending
- `STRIPE_SECRET_KEY` - Stripe API key for payment processing
- `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET` - Google OAuth credentials

## WhatsApp Integration
The platform integrates with WhatsApp using the free `wa.me` API instead of Twilio. This allows direct customer communication without extra costs.