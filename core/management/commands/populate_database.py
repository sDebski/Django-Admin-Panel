from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "This is a command populating database and creating admin user"

    def create_admin_user():
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(username="admin", password="admin")

    def handle(self, *args, **kwargs):
        self.create_admin_user()

        # TODO
        # after creating models
        # check if database already populated
        # if not -> populate
        self.stdout.write(self.style.SUCCESS("Database populated."))
