from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
import random
import string

from .models import BlockedDate, ConsultationReport, UserReading, Service

def generate_otp():
    """Generate a 6-digit OTP code"""
    return ''.join(random.choices(string.digits, k=6))

# We'll define these standalone, not inheriting from allauth forms directly
class CustomRegisterForm(forms.Form):
    """
    Custom registration form that includes phone number field
    """
    first_name = forms.CharField(max_length=30, label=_('First Name'), required=True)
    last_name = forms.CharField(max_length=30, label=_('Last Name'), required=True)
    email = forms.EmailField(label=_('Email Address'), required=True)
    username = forms.CharField(max_length=150, label=_('Username'), required=True)
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput, required=True)
    phone_number = PhoneNumberField(label=_('Phone Number'), required=True,
                                   help_text=_('We will send you a verification code to this number'))
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('This username is already taken.'))
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('This email is already registered.'))
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', _("The two password fields didn't match."))
        
        return cleaned_data

class OTPVerificationForm(forms.Form):
    """
    Form for OTP verification
    """
    otp_code = forms.CharField(max_length=6, min_length=6, label=_('Verification Code'),
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 6-digit code'}))

class ContactForm(forms.Form):
    """
    Contact form
    """
    name = forms.CharField(max_length=100, label=_('Your Name'), 
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_('Email Address'),
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(max_length=200, label=_('Subject'),
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label=_('Message'),
                             widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

class BookingForm(forms.Form):
    """
    Booking form for astrology consultation
    """
    service = forms.ChoiceField(label=_('Service'), 
                               choices=[],  # Will be populated in __init__
                               widget=forms.Select(attrs={'class': 'form-control'}))
    date = forms.DateField(label=_('Date'),
                          widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    time = forms.ChoiceField(label=_('Time'),
                            choices=[],  # Will be populated in views
                            widget=forms.Select(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100, label=_('Your Name'),
                          widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label=_('Email Address'),
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = PhoneNumberField(label=_('Phone Number'), required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(label=_('Special Requests or Notes'), required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    create_account = forms.BooleanField(label=_('Create an account'), required=False, 
                                       initial=True,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    def __init__(self, *args, **kwargs):
        services = kwargs.pop('services', [])
        time_slots = kwargs.pop('time_slots', [])
        super(BookingForm, self).__init__(*args, **kwargs)
        
        # Populate service choices
        self.fields['service'].choices = [(s.id, f"{s.name} (£{s.price})") for s in services]
        
        # Populate time slot choices if provided
        if time_slots:
            self.fields['time'].choices = [(slot, slot) for slot in time_slots]
        else:
            self.fields['time'].choices = [('', _('Select a date first'))]
            
    def clean_date(self):
        date = self.cleaned_data.get('date')
        today = timezone.now().date()
        
        if date < today:
            raise forms.ValidationError(_("You cannot book appointments in the past."))
            
        # Check if date is blocked
        if BlockedDate.objects.filter(date=date).exists():
            raise forms.ValidationError(_("This date is not available for booking."))
            
        return date

class CouponForm(forms.Form):
    """
    Coupon code form
    """
    code = forms.CharField(max_length=20, label=_('Coupon Code'),
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

class CustomLoginForm(AuthenticationForm):
    """
    Custom login form with styled widgets
    """
    username = forms.CharField(
        label=_('Username or Email'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username or Email'})
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=False,
        label=_('Remember Me'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
class ConsultationReportForm(forms.ModelForm):
    """
    Form for creating/editing consultation reports
    """
    class Meta:
        model = ConsultationReport
        fields = ['user', 'title', 'description', 'report_file', 'consultation_date']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'report_file': forms.FileInput(attrs={'class': 'form-control'}),
            'consultation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
class UserReadingForm(forms.ModelForm):
    """
    Form for creating/editing user readings
    """
    class Meta:
        model = UserReading
        fields = ['user', 'title', 'content', 'reading_date', 'is_public', 'pdf_report']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'reading_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pdf_report': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ServiceForm(forms.ModelForm):
    """
    Form for creating/editing astrology services
    """
    class Meta:
        model = Service
        fields = ['name', 'slug', 'description', 'short_description', 'price', 'duration', 'image', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'step': '15'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'duration': _('Duration in minutes'),
            'slug': _('URL-friendly name (auto-generated if left blank)'),
        }