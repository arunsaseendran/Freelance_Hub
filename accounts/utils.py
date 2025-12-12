from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailOTP


def send_otp_email(email):
    """Generate and send OTP to the given email address"""
    try:
        # Generate OTP
        otp_record = EmailOTP.generate_otp(email)
        
        # Email subject and content
        subject = 'FreelanceHub - Email Verification OTP'
        
        # Create HTML email content
        html_message = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 28px;">FreelanceHub</h1>
                <p style="color: white; margin: 10px 0 0 0; opacity: 0.9;">Email Verification</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px;">
                <h2 style="color: #333; margin-bottom: 20px;">Verify Your Email Address</h2>
                
                <p style="color: #666; font-size: 16px; line-height: 1.6;">
                    Thank you for registering with FreelanceHub! To complete your registration, 
                    please use the following One-Time Password (OTP):
                </p>
                
                <div style="background: white; border: 2px dashed #667eea; border-radius: 10px; padding: 20px; text-align: center; margin: 25px 0;">
                    <div style="font-size: 32px; font-weight: bold; color: #667eea; letter-spacing: 8px; font-family: monospace;">
                        {otp_record.otp}
                    </div>
                </div>
                
                <p style="color: #666; font-size: 14px; line-height: 1.6;">
                    <strong>Important:</strong><br>
                    • This OTP is valid for 10 minutes only<br>
                    • Do not share this OTP with anyone<br>
                    • If you didn't request this, please ignore this email
                </p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; text-align: center;">
                    <p style="color: #999; font-size: 12px; margin: 0;">
                        This is an automated email from FreelanceHub. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </div>
        """
        
        # Plain text version
        plain_message = f"""
        FreelanceHub - Email Verification
        
        Thank you for registering with FreelanceHub!
        
        Your OTP for email verification is: {otp_record.otp}
        
        This OTP is valid for 10 minutes only.
        Do not share this OTP with anyone.
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        FreelanceHub Team
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return True, "OTP sent successfully"
        
    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}"


def verify_otp(email, entered_otp):
    """Verify the OTP for the given email"""
    try:
        otp_record = EmailOTP.objects.filter(
            email=email,
            is_verified=False
        ).latest('created_at')
        
        return otp_record.verify(entered_otp)
        
    except EmailOTP.DoesNotExist:
        return False, "No OTP found for this email"
