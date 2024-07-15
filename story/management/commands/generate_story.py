from django.core.management.base import BaseCommand, CommandError

from core import models

import ollama

from langchain_core.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        prompt_prefix = """
I want to you to create a bedtime story for kids under 6 age. Below I give you a sample story. 
After the sample story, I will give you the information to use to generate the story. 
I want you to write the topic in the first line and start the story after it. 
Your respond should only contain the title and the story.
"""

        trigger = models.StoryTrigger.objects.order_by("id").first()
        sample_stories = models.Story.objects.filter(language="en").exclude(
            story_trigger__isnull=True
        )
        example_stories = []

        for story in sample_stories:
            example_stories.append(
                {
                    "setting": story.story_trigger.setting_str_for_prompt,
                    "story": story.title + "\n" + story.text,
                }
            )

        example_prompt = ChatPromptTemplate.from_messages(
            [
                ("user", "{setting}"),
                ("assistant", "{story}"),
            ]
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            example_prompt=example_prompt,
            examples=example_stories,
        )

        final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt_prefix),
                few_shot_prompt,
                ("user", "{setting}"),
            ]
        )

        client = ollama.Client(host="http://ollama:11434")

        response = client.chat(
            model="llama3:latest",
            messages=[
                {
                    "role": "user",
                    "content": final_prompt.format(
                        setting=trigger.setting_str_for_prompt
                    ),
                },
            ],
        )

        print(f"Response: {response['message']['content']}")
