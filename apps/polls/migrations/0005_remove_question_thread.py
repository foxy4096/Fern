# Generated by Django 4.2.4 on 2023-10-14 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_alter_question_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='thread',
        ),
    ]
