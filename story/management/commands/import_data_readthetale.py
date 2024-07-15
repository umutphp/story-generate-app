from django.core.management.base import BaseCommand, CommandError

import requests, re
from bs4 import BeautifulSoup

from core import models


class Command(BaseCommand):
    BASE_URL = "https://www.readthetale.com/"

    def handle(self, *args, **options):
        stories = {}

        try:
            response = requests.get(f"{self.BASE_URL}popular-bedtime-stories")
            soup = BeautifulSoup(response.text, "html.parser")
        except:
            raise CommandError("Error fetching data from readthetale.")

        story_links = soup.find_all("a", class_=re.compile("XqQF9c"), href=True)

        for story_link in story_links:
            if story_link["href"].startswith(r"/popular-bedtime-stories/"):
                stories[story_link["href"]] = story_link.text

        for story_url in stories:
            print("Started fetching the story: ", story_url, stories[story_url])

            try:
                response = requests.get(f"{self.BASE_URL}{story_url}")
                soup = BeautifulSoup(response.text, "html.parser")
                story_texts = soup.find_all("span", class_=re.compile("gBYvFf C9DxTc"))

                merged_story_text = ""
                for story_text in story_texts:
                    merged_story_text += story_text.text + "\n\n"

                print("Saving the story...")
                models.Story.objects.create(
                    title=stories[story_url],
                    text=merged_story_text,
                    language="en",
                    generated=False,
                )
            except:
                print("Error in fetching story!!!")
                continue
