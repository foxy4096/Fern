# Generated by Django 4.2.4 on 2023-08-27 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_alter_post_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Select category for this post.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forum.category', verbose_name='Category'),
        ),
    ]