from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create n number of user'

    def handle(self, *args, **options):

        for i in range(1, 31):
            username = f"user{i}"
            if not User.objects.filter(username=username).exists():
                user = User(username=username)
                user.set_password('1234')
                user.save()
                print(f"User {username} created successfully.")
            else:
                print(f"User {username} already exists.")

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {30} services!')
        )
