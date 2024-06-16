# Generated by Django 3.2.25 on 2024-06-15 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20240615_2302'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryTrigger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(default='tr', max_length=5)),
                ('place', models.CharField(max_length=256)),
                ('topic', models.CharField(max_length=256)),
                ('characters', models.JSONField()),
            ],
        ),
    ]