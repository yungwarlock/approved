import glob
import json
from datetime import datetime

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError

from companies.models import Company


class Command(BaseCommand):
    help = "Import data from folder"

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str)

    def create_company(self, data):
        return Company.objects.create(  # type: ignore
            name=data.get("name", ""),
            slug=data.get("slug", ""),
            about=data.get("about", ""),
            twitter=data.get("twitter", ""),
            website=data.get("website", ""),
            location=data.get("location", ""),
            logo_url=data.get(
                "logo_url", f"https://logo.clearbit.com/{data.get('website', '')}"),
            date_founded=data.get("date_founded") if data.get(
                "date_founded", "") else datetime.now().date(),
        )

    def handle(self, *args, **options):
        folder_name = options["folder"]

        with transaction.atomic():
            for file_name in glob.glob(folder_name + "/*.json"):
                with open(file_name) as f:
                    data = json.load(f)
                    self.create_company(data)

        self.stdout.write(
            self.style.SUCCESS(  # type: ignore
                f"Successfully imported data from {folder_name}")
        )
