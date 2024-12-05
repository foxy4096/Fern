# Generated by Django 4.2.4 on 2023-11-10 17:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_alter_choice_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='voted_by',
            field=models.ManyToManyField(blank=True, related_name='voted_choices', to=settings.AUTH_USER_MODEL, verbose_name='Votes'),
        ),
    ]