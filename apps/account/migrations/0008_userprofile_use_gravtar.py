# Generated by Django 4.2.4 on 2023-11-01 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_userprofile_rank'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='use_gravtar',
            field=models.BooleanField(default=True, help_text='Use Gravatar instead of a profile picture', verbose_name='Use Gravatar'),
        ),
    ]
