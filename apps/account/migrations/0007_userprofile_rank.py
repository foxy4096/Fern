# Generated by Django 4.2.4 on 2023-10-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_userprofile_location_userprofile_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='rank',
            field=models.IntegerField(default=0, help_text='The rank of the user in the leaderboard', verbose_name='Rank'),
        ),
    ]
