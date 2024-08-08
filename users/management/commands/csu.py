from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Класс для кастомной команды создания суперпользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(email='admin@sky.pro')
        user.set_password('admin123')
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
