import os

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp


class Command(BaseCommand):
    help = "Create/update the Google SocialApp for production"

    def handle(self, *args, **options):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    "GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET is not set."
                )
            )
            return

        site = Site.objects.get_or_create(
            id=2,
            defaults={
                "domain": "taskend.onrender.com",
                "name": "TaskEnd",
            },
        )[0]

        site.domain = "taskend.onrender.com"
        site.name = "TaskEnd"
        site.save()

        app, created = SocialApp.objects.update_or_create(
            provider="google",
            defaults={
                "name": "Google",
                "client_id": client_id,
                "secret": client_secret,
            },
        )

        app.sites.set([site])

        if created:
            self.stdout.write(
                self.style.SUCCESS("Google SocialApp created successfully.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("Google SocialApp updated successfully.")
            )