from django.core.management.commands.startapp import Command as StartAppCommand
import os

SERVICE_CONFIG_TEMPLATE = '''from django.apps import AppConfig
from django.db.utils import OperationalError

class {class_name}(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "{app_name}"
    verbose_name = "{verbose_name}"

    def ready(self):
        from saas.models import Service  # adjust import path
        try:
            Service.objects.get_or_create(
                name=self.verbose_name,
                defaults={{
                    "description": f"{{self.verbose_name}} service",
                    "workflow": {{}},
                    "config": {{}}
                }}
            )
        except OperationalError:
            # DB not ready during migration
            pass
'''

class Command(StartAppCommand):
    help = "Creates a new Django app, with optional --service flag to auto-register in Service model"

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "--service",
            action="store_true",
            help="Configure app as a Service (auto-register in Service model)"
        )

    def handle(self, *args, **options):
        super().handle(*args, **options)

        app_name = options["name"]
        if options["service"]:
            app_dir = os.path.join(os.getcwd(), app_name)
            apps_file = os.path.join(app_dir, "apps.py")

            class_name = f"{app_name.capitalize()}Config"
            verbose_name = app_name.replace("_", " ").title()

            with open(apps_file, "w") as f:
                f.write(SERVICE_CONFIG_TEMPLATE.format(
                    class_name=class_name,
                    app_name=app_name,
                    verbose_name=verbose_name
                ))

            self.stdout.write(
                self.style.SUCCESS(f"✔ Created service app '{app_name}' with auto-registration in Service model")
            )
