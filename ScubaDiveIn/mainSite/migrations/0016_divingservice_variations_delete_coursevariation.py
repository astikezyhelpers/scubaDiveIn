# Generated by Django 4.2.20 on 2025-05-19 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0015_alter_divingservice_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='divingservice',
            name='variations',
            field=models.JSONField(blank=True, help_text="Course variations stored as JSON. Format: [{'id': 'str', 'name': 'str', 'price': float, 'duration': int, 'max_participants': int}]", null=True),
        ),
        migrations.DeleteModel(
            name='CourseVariation',
        ),
    ]
