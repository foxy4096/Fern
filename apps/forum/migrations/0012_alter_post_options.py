# Generated by Django 4.2.4 on 2023-10-12 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0011_alter_thread_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['created_at']},
        ),
    ]
