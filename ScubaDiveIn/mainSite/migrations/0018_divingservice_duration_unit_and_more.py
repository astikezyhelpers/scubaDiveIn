# Generated by Django 4.2.20 on 2025-05-19 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainSite', '0017_alter_divingservice_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='divingservice',
            name='duration_unit',
            field=models.CharField(choices=[('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days')], default='minutes', help_text='Unit for the duration', max_length=10),
        ),
        migrations.AlterField(
            model_name='divingservice',
            name='duration',
            field=models.PositiveIntegerField(help_text='Base duration value'),
        ),
    ]
