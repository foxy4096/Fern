# Generated by Django 4.2.4 on 2023-10-14 12:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0005_remove_question_thread'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='voted_by',
            field=models.ManyToManyField(blank=True, related_name='voted_questions', to=settings.AUTH_USER_MODEL, verbose_name='Votes'),
        ),
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='No. of Votes'),
        ),
    ]