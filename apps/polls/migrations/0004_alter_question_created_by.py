# Generated by Django 4.2.4 on 2023-10-14 11:43

import apps.account.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0003_question_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=models.SET(apps.account.models.get_sentinel_user), related_name='questions', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
            preserve_default=False,
        ),
    ]
