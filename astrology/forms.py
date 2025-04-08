from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
import random
import string

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
    phone = PhoneNumberField(label=_('Phone Number'),
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(label=_('Special Requests or Notes'), required=False,
                           widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    
    def __init__(self, *args, **kwargs):
        services = kwargs.pop('services', [])
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['service'].choices = [(s.id, f"{s.name} (£{s.price})") for s in services]

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