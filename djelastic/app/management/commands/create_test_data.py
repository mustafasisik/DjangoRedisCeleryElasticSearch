from django.core.management.base import BaseCommand

from app.models import *

# from app.models import *


class Command(BaseCommand):
    help = 'Create admin user if not exists'

    def handle(self, *args, **options):

        if not Server.objects.exists():
            server = Server()
            server.hostname = "octoxlabs"
            server.ip = "12.34.212.34"
            server.save()

            self.stdout.write(self.style.SUCCESS('Server Created Successfully'))



