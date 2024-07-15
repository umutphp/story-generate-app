from django.core.management.base import BaseCommand, CommandError

from datasets import load_dataset
from core import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            dataset = load_dataset("umutphp/masallar", split="train")
        except:
            raise CommandError("Error fetching dataset from remote.")

        models.Story.objects.all().delete()

        for story in dataset:
            print(f"Saving the story with title={story['title']}...")
            models.Story.objects.create(
                title=story["title"],
                text=story["text"],
                area=story["area"],
                city=story["city"],
                language="tr",
                generated=False,
            )
