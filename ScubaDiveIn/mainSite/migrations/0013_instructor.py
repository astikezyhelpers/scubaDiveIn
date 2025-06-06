# Generated by Django 4.2.20 on 2025-05-18 12:35

from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0012_remove_instructorbooking_admin_notes_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('experience_years', models.IntegerField()),
                ('total_dives', models.IntegerField()),
                ('description', models.TextField()),
                ('specialties', models.JSONField(default=list)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='instructors/')),
                ('certificate_image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to='certificates/')),
            ],
        ),
    ]
