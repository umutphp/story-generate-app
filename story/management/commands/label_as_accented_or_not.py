from django.core.management.base import BaseCommand, CommandError

from core import models

import ollama
import nltk


def summary(sentences):
    return sentences[0].replace("&nbsp;", "") + ' ' + sentences[1].replace("&nbsp;", "") + ' ' + sentences[2].replace("&nbsp;", "") + ' ' + sentences[3].replace("&nbsp;", "")


class Command(BaseCommand):
    def handle(self, *args, **options):
        nltk.download('punkt')

        dataset = models.Story.objects.filter(accented__isnull=True)

        prompt = "Sen verilen talimatları takip ederek en iyi cevabı üretmeye çalışan yardımcı bir yapay zekasın."
        prompt = (prompt + "\n\n" + "Aşağıdaki cümleler düzgün bir Türkçe ile yazılmış ise " +
                  "sadece '1', aksanlı bir dil ile yazılmışsa sadece '0' şeklinde cevaplar mısın?")

        client = ollama.Client(host="http://ollama:11434")

        for story in dataset:
            print("---------------------------------------------")
            print(f"Labelling {story.title}...")

            sentences = nltk.sent_tokenize(story.text)

            print(summary(sentences))

            response = client.chat(model='llama3:latest', messages=[
                {
                    'role': 'user',
                    'content': prompt + "\n\n" + summary(sentences),
                },
            ])

            print(f"Response: {response['message']['content']}")
            print("---------------------------------------------")

            if response['message']['content'] == '1':
                story.accented = False

            if response['message']['content'] == '0':
                story.accented = True

            story.save()
