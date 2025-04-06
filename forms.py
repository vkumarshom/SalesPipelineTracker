from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, DateField, TimeField, FloatField, SubmitField, HiddenField, EmailField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Optional
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Send Message')

class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=120)])
    slug = StringField('Slug', validators=[DataRequired(), Length(min=3, max=120)])
    summary = StringField('Summary', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=256)])
    published = BooleanField('Published')
    submit = SubmitField('Save Post')

class ServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=100)])
    slug = StringField('Slug', validators=[DataRequired(), Length(min=3, max=100)])
    short_description = StringField('Short Description', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    duration = SelectField('Duration (minutes)', choices=[(30, '30 min'), (60, '60 min'), (90, '90 min'), (120, '120 min')], coerce=int, validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Length(max=256)])
    is_available = BooleanField('Available')
    submit = SubmitField('Save Service')

class BookingForm(FlaskForm):
    service_id = SelectField('Service', coerce=int, validators=[DataRequired()])
    booking_date = DateField('Date', validators=[DataRequired()])
    booking_time = SelectField('Time', validators=[DataRequired()], choices=[
        ('09:00', '9:00 AM'), ('10:00', '10:00 AM'), ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'), ('13:00', '1:00 PM'), ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'), ('16:00', '4:00 PM'), ('17:00', '5:00 PM')
    ])
    customer_name = StringField('Name', validators=[DataRequired(), Length(min=3, max=100)])
    customer_email = EmailField('Email', validators=[DataRequired(), Email()])
    customer_phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Book Appointment')
    
    def validate_booking_date(self, field):
        if field.data < date.today():
            raise ValidationError('Booking date cannot be in the past.')

class CheckoutForm(FlaskForm):
    customer_name = StringField('Full Name', validators=[DataRequired(), Length(min=3, max=100)])
    customer_email = EmailField('Email', validators=[DataRequired(), Email()])
    customer_phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    submit = SubmitField('Complete Purchase')
