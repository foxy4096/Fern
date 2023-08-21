# Generated by Django 4.2.4 on 2023-08-21 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.post', verbose_name='Reply To'),
        ),
    ]