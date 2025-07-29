"""
Management command to test email configuration for EcoConnect
Usage: python manage.py test_email your-email@example.com
"""

from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email configuration by sending a test email'

    def add_arguments(self, parser):
        parser.add_argument(
            'email', 
            type=str, 
            help='Email address to send test email to'
        )

    def handle(self, *args, **options):
        test_email = options['email']
        
        self.stdout.write(f'Testing email configuration...')
        self.stdout.write(f'Sending test email to: {test_email}')
        self.stdout.write(f'From: {settings.DEFAULT_FROM_EMAIL}')
        self.stdout.write(f'Email Backend: {settings.EMAIL_BACKEND}')
        
        try:
            # Send test email
            send_mail(
                subject='🌱 EcoConnect - Email Test SUCCESS',
                message=f'''
🌱 EcoConnect - Email Configuration Test

SUCCESS! Your email configuration is working correctly.

Configuration Details:
- Email Backend: {settings.EMAIL_BACKEND}
- From Address: {settings.DEFAULT_FROM_EMAIL}
- Test Status: ✅ PASSED

What works now:
✅ Password reset emails
✅ Contact form submissions
✅ Welcome emails (if implemented)
✅ Event notifications (if implemented)

Next Steps: Test the password reset functionality at your EcoConnect login page!

---
EcoConnect - Connecting communities for environmental action
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[test_email],
                fail_silently=False,
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Successfully sent test email to {test_email}')
            )
            self.stdout.write(
                self.style.SUCCESS('🎉 Your email configuration is working properly!')
            )
            self.stdout.write(
                'Next: Try the password reset feature at /users/password-reset/'
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to send email: {str(e)}')
            )
            self.stdout.write(
                self.style.WARNING('Troubleshooting tips:')
            )
            self.stdout.write('1. Check your .env file has the correct API key')
            self.stdout.write('2. Verify your SendGrid account is active')
            self.stdout.write('3. Ensure your API key has Mail Send permissions')
            self.stdout.write('4. Check if your domain is verified (for custom from addresses)')
            
        self.stdout.write('\nCurrent Settings:')
        self.stdout.write(f'EMAIL_BACKEND: {settings.EMAIL_BACKEND}')
        self.stdout.write(f'EMAIL_HOST: {getattr(settings, "EMAIL_HOST", "Not set")}')
        self.stdout.write(f'EMAIL_PORT: {getattr(settings, "EMAIL_PORT", "Not set")}')
        self.stdout.write(f'DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}')