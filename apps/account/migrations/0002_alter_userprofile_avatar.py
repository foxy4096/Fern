# Generated by Django 4.2.4 on 2023-08-21 10:54

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=django_resized.forms.ResizedImageField(crop=['middle', 'center'], default='default/avatar.png', force_format=None, keep_meta=True, quality=-1, scale=None, size=[600, 600], upload_to='avatars', verbose_name='Profile Picture'),
        ),
    ]
