# Generated by Django 4.2.4 on 2023-11-07 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]