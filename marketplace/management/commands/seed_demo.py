from django.core.management.base import BaseCommand
from .ensure_demo_data import Command as EnsureDemoDataCommand


class Command(BaseCommand):
    help = "Backward-compatible alias: safely add/update demo cafés without deleting existing records."

    def handle(self, *args, **options):
        EnsureDemoDataCommand().handle(*args, **options)
