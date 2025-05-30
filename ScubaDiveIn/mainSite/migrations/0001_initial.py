# Generated by Django 4.2.20 on 2025-05-07 03:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DivingService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('short_description', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=10)),
                ('duration', models.PositiveIntegerField(help_text='Duration in minutes')),
                ('max_participants', models.PositiveIntegerField(default=10)),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], db_index=True, default='beginner', max_length=20)),
                ('included_items', models.TextField(blank=True, help_text='Items included in the service, one per line')),
                ('requirements', models.TextField(blank=True, help_text='Requirements for this service, one per line')),
                ('featured_image', models.ImageField(blank=True, null=True, upload_to='service_images/')),
                ('is_featured', models.BooleanField(db_index=True, default=False)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['category', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_gallery/')),
                ('caption', models.CharField(blank=True, max_length=200)),
                ('order', models.PositiveIntegerField(default=0)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='mainSite.divingservice')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, help_text='Display order on the website')),
            ],
            options={
                'verbose_name_plural': 'Service Categories',
                'ordering': ['order', 'name'],
                'indexes': [models.Index(fields=['order', 'name'], name='mainSite_se_order_93d9bc_idx')],
            },
        ),
        migrations.AddField(
            model_name='divingservice',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='mainSite.servicecategory'),
        ),
        migrations.CreateModel(
            name='RazorpayPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(db_index=True, max_length=100)),
                ('payment_id', models.CharField(blank=True, db_index=True, max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currency', models.CharField(default='INR', max_length=10)),
                ('status', models.CharField(choices=[('created', 'Created'), ('attempted', 'Attempted'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], db_index=True, default='created', max_length=20)),
                ('booking_date', models.DateField(blank=True, db_index=True, null=True)),
                ('participants', models.PositiveIntegerField(default=1)),
                ('customer_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='mainSite.divingservice')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['user', 'status'], name='mainSite_ra_user_id_508a0c_idx'), models.Index(fields=['service', 'booking_date'], name='mainSite_ra_service_aa9699_idx'), models.Index(fields=['created_at'], name='mainSite_ra_created_b5c7af_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='divingservice',
            index=models.Index(fields=['category', 'name'], name='mainSite_di_categor_b1c9cd_idx'),
        ),
        migrations.AddIndex(
            model_name='divingservice',
            index=models.Index(fields=['is_featured', 'is_active'], name='mainSite_di_is_feat_555215_idx'),
        ),
        migrations.AddIndex(
            model_name='divingservice',
            index=models.Index(fields=['difficulty_level'], name='mainSite_di_difficu_55b2ed_idx'),
        ),
    ]
