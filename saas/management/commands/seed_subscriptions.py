import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from saas import models
from saas.models import Service, Status

class Command(BaseCommand):
    help = 'Assign random subscriptions to all users'

    def handle(self, *args, **options):
        services = list(Service.objects.all())
        if not services:
            self.stdout.write(self.style.WARNING('No services found. Please create services first.'))
            return

        for user in User.objects.all():
            subscribed_services = random.sample(services, k=random.randint(1, min(3, len(services))))
            for service in subscribed_services:
                subscription, created = models.Subscription.objects.get_or_create(
                    service=service,
                    created_by=user,
                    defaults={
                        "active": True,
                        "status": Status.CONFIRMED
                    }
                )
                if created:
                    print(f"{user.username} subscribed to {service.name}")

        self.stdout.write(
            self.style.SUCCESS('Successfully created subscriptions for all users!')
        )
