from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings
from core import models


User = get_user_model()
import os


class Command(BaseCommand):
    help = "This is a command populating database and creating admin user"

    def create_admin_user(self):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin")

    def handle(self, *args, **kwargs):
        self.create_admin_user()

        database_populated = models.Project.objects.all().exists()
        if database_populated:
            return
        for dir in settings.FIXTURE_DIRS:
            for file in os.listdir(dir):
                if file.endswith(".json"):
                    call_command("loaddata", file)
        self.stdout.write(self.style.SUCCESS("Database populated."))
