from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import User, FreelancerProfile, CustomerProfile, EmailOTP
import re

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address'
        }),
        help_text="We'll send an OTP to verify your email"
    )
    
    phone = forms.CharField(
        max_length=15,
        required=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+91 9876543210'
        })
    )
    
    user_type = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('freelancer', 'Freelancer')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )
    
    pincode = forms.CharField(
        max_length=6,
        required=True,
        validators=[RegexValidator(
            regex=r'^\d{6}$',
            message="Pincode must be exactly 6 digits."
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '123456'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 
                  'phone', 'user_type', 'city', 'area', 'pincode', 'address']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add custom attributes to fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a unique username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your city'
        })
        self.fields['area'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your area/locality'
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your full address',
            'rows': 3
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        return username
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise ValidationError("A user with this phone number already exists.")
        return phone


class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        min_length=6,
        required=True,
        validators=[RegexValidator(
            regex=r'^\d{6}$',
            message="OTP must be exactly 6 digits."
        )],
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': '123456',
            'style': 'font-size: 1.5rem; letter-spacing: 0.5rem;',
            'maxlength': '6'
        }),
        help_text="Enter the 6-digit OTP sent to your email"
    )
    
    def __init__(self, email, *args, **kwargs):
        self.email = email
        super().__init__(*args, **kwargs)
    
    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        try:
            otp_record = EmailOTP.objects.filter(
                email=self.email,
                is_verified=False
            ).latest('created_at')
            
            is_valid, message = otp_record.verify(otp)
            if not is_valid:
                raise ValidationError(message)
            
        except EmailOTP.DoesNotExist:
            raise ValidationError("No OTP found for this email. Please request a new one.")
        
        return otp


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'area', 'pincode', 'profile_picture']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['bio', 'experience_years', 'skills', 'payment_mode', 'gpay_number', 
                  'hourly_rate', 'is_available']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'is_available':
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
