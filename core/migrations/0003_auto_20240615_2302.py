# Generated by Django 3.2.25 on 2024-06-15 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_story_accented'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='generated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='story',
            name='language',
            field=models.CharField(default='tr', max_length=5),
        ),
    ]