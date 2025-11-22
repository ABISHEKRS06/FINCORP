from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if one does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@fincorp.com',
                password='FinCorp@2025'
            )
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser "admin" already exists'))
