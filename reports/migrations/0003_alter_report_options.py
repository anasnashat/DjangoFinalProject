# Generated by Django 5.2.1 on 2025-05-25 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_remove_report_replay_report_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ['-created_at']},
        ),
    ]
