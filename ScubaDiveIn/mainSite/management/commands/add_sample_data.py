from django.core.management.base import BaseCommand
from mainSite.models import ServiceCategory, DivingService
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Adds sample data for services and categories'

    def handle(self, *args, **kwargs):
        # Create DSD category
        dsd_category, created = ServiceCategory.objects.get_or_create(
            name="Discover Scuba Diving",
            defaults={
                'description': "Experience the thrill of scuba diving for the first time",
                'order': 1
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Created category: {dsd_category.name}'))

        # Create DSD course
        dsd_course, created = DivingService.objects.get_or_create(
            name="Discover Scuba Diving",
            defaults={
                'slug': 'discover-scuba-diving',
                'category': dsd_category,
                'short_description': "Experience your first breath underwater in a safe and controlled environment",
                'description': """
                Take your first step into the underwater world with our Discover Scuba Diving program.
                Perfect for beginners, this introductory course lets you:
                - Experience breathing underwater
                - Learn basic diving skills
                - Explore a shallow reef with a professional instructor
                - Get a taste of the amazing underwater world
                
                No prior experience needed! Our expert instructors will guide you through every step.
                """,
                'price': 4999.00,
                'duration': 180,  # 3 hours
                'max_participants': 4,
                'difficulty_level': 'beginner',
                'included_items': """
                - All scuba diving equipment
                - Professional PADI instructor
                - Pool session
                - Open water dive
                - Certificate of completion
                - Photos of your experience
                """,
                'requirements': """
                - Minimum age: 10 years
                - Comfortable in water
                - Basic swimming ability
                - Good physical health
                - Signed liability release
                """,
                'is_featured': True,
                'is_active': True
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Created DSD course: {dsd_course.name}'))
        self.stdout.write(self.style.SUCCESS('Successfully added sample data')) 