"""
Management command to check user emails in the database
Usage: python manage.py check_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check all users and their email addresses'

    def handle(self, *args, **options):
        self.stdout.write('=== USER EMAIL CHECK ===\n')
        
        users = User.objects.all()
        total_users = users.count()
        users_with_email = users.exclude(email='').count()
        
        self.stdout.write(f'Total users: {total_users}')
        self.stdout.write(f'Users with email: {users_with_email}')
        self.stdout.write(f'Users without email: {total_users - users_with_email}\n')
        
        self.stdout.write('User List:')
        self.stdout.write('-' * 60)
        
        for user in users:
            email_status = '✅' if user.email else '❌ NO EMAIL'
            self.stdout.write(
                f'Username: {user.username:<20} '
                f'Email: {user.email if user.email else "NOT SET":<30} '
                f'{email_status}'
            )
        
        self.stdout.write('\n' + '=' * 60)
        
        if users_with_email < total_users:
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠️  Some users don\'t have email addresses set!'
                )
            )
            self.stdout.write(
                'Password reset will only work for users with email addresses.\n'
            )
            
            # Show how to fix
            self.stdout.write('To add an email to a user, run:')
            self.stdout.write('python manage.py shell')
            self.stdout.write('>>> from django.contrib.auth.models import User')
            self.stdout.write('>>> user = User.objects.get(username="USERNAME")')
            self.stdout.write('>>> user.email = "user@example.com"')
            self.stdout.write('>>> user.save()')
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ All users have email addresses!')
            )