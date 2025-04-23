from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create a superuser non-interactively for CustomUser'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv('SUPERUSER_USERNAME', 'bongbong')
        email = os.getenv('SUPERUSER_EMAIL', 'bongbong@gmail.com')
        password = os.getenv('SUPERUSER_PASSWORD', 'Carl@123')
        first_name = os.getenv('SUPERUSER_FIRST_NAME', 'Bongbong')
        last_name = os.getenv('SUPERUSER_LAST_NAME', 'User')
        contact = os.getenv('SUPERUSER_CONTACT', '1234567890')
        address = os.getenv('SUPERUSER_ADDRESS', '123 Main St')
        gender = os.getenv('SUPERUSER_GENDER', 'Male')

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Superuser {email} already exists.'))
            return

        try:
            User.objects.create_superuser(
                email=email,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                contact=contact,
                address=address,
                gender=gender,
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully.'))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {e}'))