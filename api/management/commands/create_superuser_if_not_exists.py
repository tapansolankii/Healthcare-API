from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='tapansolanki').exists():
            User.objects.create_superuser('tapansolanki', 'tapan@example.com', 'new12345')
            self.stdout.write(self.style.SUCCESS('Superuser "tapansolanki" created successfully (if it did not exist).'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser "tapansolanki" already exists.')) 