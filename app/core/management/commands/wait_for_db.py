"""Django Wait for db commands"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """Django command to wait for db"""

    def handle(self, *args, **options):
        pass