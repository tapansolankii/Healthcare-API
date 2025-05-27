from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'tapansolanki')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'tapan@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'new12345')

        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating superuser: {str(e)}')) 