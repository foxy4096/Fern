# Generated by Django 4.2.4 on 2023-08-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, help_text='Markdown and BBCode Supported', max_length=500, verbose_name='Description'),
        ),
    ]
