from django.core.management.base import BaseCommand
from mainSite.models import ServiceCategory, DivingService, ServiceImage
from django.core.files import File
from pathlib import Path
import os

class Command(BaseCommand):
    help = 'Adds sample data for services and categories'

    def handle(self, *args, **kwargs):
        # Create a sample category
        category, created = ServiceCategory.objects.get_or_create(
            name="Beginner Diving",
            defaults={
                'description': "Perfect for first-time divers and beginners",
                'order': 1
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Create a sample service
        service, created = DivingService.objects.get_or_create(
            name="Basic Scuba Diving Course",
            defaults={
                'slug': 'basic-scuba-diving-course',
                'category': category,
                'short_description': "Learn the basics of scuba diving in a safe and controlled environment",
                'description': """
                This comprehensive course is designed for beginners who want to experience the underwater world.
                You'll learn:
                - Basic diving equipment and its use
                - Underwater communication
                - Safety procedures
                - Basic diving techniques
                """,
                'price': 4999.00,
                'duration': 180,  # 3 hours
                'max_participants': 6,
                'difficulty_level': 'beginner',
                'included_items': """
                - All diving equipment
                - Professional instructor
                - Training materials
                - Certificate of completion
                """,
                'requirements': """
                - Minimum age: 12 years
                - Basic swimming ability
                - Good physical health
                """,
                'is_featured': True,
                'is_active': True
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Created service: {service.name}'))

        # Create sample images directory if it doesn't exist
        media_dir = Path('media/service_images')
        media_dir.mkdir(parents=True, exist_ok=True)

        # Add sample images
        sample_images = [
            {
                'caption': 'Diving Equipment',
                'order': 1
            },
            {
                'caption': 'Underwater Training',
                'order': 2
            },
            {
                'caption': 'Group Diving Session',
                'order': 3
            }
        ]

        for img_data in sample_images:
            ServiceImage.objects.get_or_create(
                service=service,
                defaults={
                    'caption': img_data['caption'],
                    'order': img_data['order']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully added sample data')) 