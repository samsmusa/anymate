from django.apps import AppConfig
from django.db.utils import OperationalError

class FacebookConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "facebook"
    verbose_name = "Facebook"

    def ready(self):
        from saas.models import Service  # adjust import path
        try:
            Service.objects.get_or_create(
                name=self.verbose_name,
                defaults={
                    "description": f"{self.verbose_name} service",
                    "workflow": {},
                    "config": {}
                }
            )
        except OperationalError:
            # DB not ready during migration
            pass
