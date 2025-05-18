import os
import csv
import django
import uuid
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScubaDiveIn.settings')
django.setup()

from mainSite.models import DiveLocation, DivingService, ServiceCategory, Event

def import_dive_sites():
    """Import dive sites from CSV"""
    print("Importing dive sites...")
    with open('../Dive_Sites.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get the data from the correct columns
            name = row.get('DIVE SITE', '')
            if not name:
                continue
                
            slug = slugify(name)
            
            # Check if the dive location already exists
            if DiveLocation.objects.filter(slug=slug).exists():
                print(f"Dive location '{name}' already exists. Skipping...")
                continue
            
            # Parse depth range
            depth_range = row.get('DEPTH (meters)', '')
            depth_min = 5
            depth_max = 30
            
            if '-' in depth_range:
                try:
                    depth_parts = depth_range.split('-')
                    depth_min = int(depth_parts[0].strip('m').strip())
                    depth_max = int(depth_parts[1].strip('m').strip())
                except (ValueError, IndexError):
                    pass
            
            # Create the dive location
            location = DiveLocation(
                name=name,
                slug=slug,
                short_description=f"Beautiful dive site with depths of {depth_range}",
                description=row.get('DESCRIPTION', 'This is a spectacular dive site in the Andaman islands with amazing marine life.'),
                boat_ride_duration=int(row.get('TRAVEL DURATION (minutes)', 30)),
                depth_range_min=depth_min,
                depth_range_max=depth_max,
                is_featured=True,  # Set all imported sites as featured initially
                is_active=True,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            location.save()
            print(f"Added dive location: {name}")

def import_courses():
    """Import courses from CSV"""
    print("Importing courses...")
    
    # Since the Courses.csv is empty, let's create some sample courses
    
    # Ensure the course category exists
    category, created = ServiceCategory.objects.get_or_create(
        name="Diving Courses"
    )
    
    # Sample course data
    sample_courses = [
        {
            'name': 'Open Water Diver Certification',
            'short_description': 'Basic certification course for beginners',
            'description': 'The Open Water Diver course is your first step into the exciting world of scuba diving. This comprehensive course teaches you all the fundamentals of scuba diving, including equipment, techniques, and safety procedures.',
            'price': 15000,
            'duration': 3 * 8 * 60,  # 3 days in minutes
            'difficulty': 'beginner',
            'is_featured': True
        },
        {
            'name': 'Advanced Open Water Diver',
            'short_description': 'Take your diving skills to the next level',
            'description': 'The Advanced Open Water Diver course expands on your basic skills and introduces you to new diving environments and activities. Perfect for those who want to explore deeper and experience more diverse diving conditions.',
            'price': 20000,
            'duration': 2 * 8 * 60,  # 2 days in minutes
            'difficulty': 'intermediate',
            'is_featured': True
        },
        {
            'name': 'Rescue Diver Course',
            'short_description': 'Learn essential emergency response skills',
            'description': 'The Rescue Diver course prepares you to handle dive emergencies. You\'ll learn to recognize, prevent, and manage dive-related problems both for yourself and other divers.',
            'price': 25000,
            'duration': 4 * 8 * 60,  # 4 days in minutes
            'difficulty': 'advanced',
            'is_featured': False
        },
        {
            'name': 'Night Diving Specialty',
            'short_description': 'Experience the magic of the underwater world at night',
            'description': 'The Night Diving Specialty course opens up a whole new world of diving. Many marine creatures are nocturnal, and you\'ll get to see behaviors and species that day divers miss out on.',
            'price': 8000,
            'duration': 1 * 8 * 60,  # 1 day in minutes
            'difficulty': 'intermediate',
            'is_featured': True
        },
        {
            'name': 'Underwater Photography Course',
            'short_description': 'Capture the beauty of the underwater world',
            'description': 'Learn how to take stunning underwater photographs with our specialized course. You\'ll master camera settings, lighting techniques, and composition principles for underwater environments.',
            'price': 12000,
            'duration': 2 * 8 * 60,  # 2 days in minutes
            'difficulty': 'beginner',
            'is_featured': True
        }
    ]
    
    for course_data in sample_courses:
        name = course_data['name']
        slug = slugify(name)
        
        # Check if the course already exists
        if DivingService.objects.filter(slug=slug).exists():
            print(f"Course '{name}' already exists. Skipping...")
            continue
        
        # Create the course
        course = DivingService(
            name=name,
            slug=slug,
            category=category,
            short_description=course_data['short_description'],
            description=course_data['description'],
            price=course_data['price'],
            duration=course_data['duration'],
            difficulty_level=course_data['difficulty'],
            is_featured=course_data['is_featured'],
            is_active=True
        )
        course.save()
        print(f"Added course: {name}")

def import_events():
    """Import events from CSV"""
    print("Importing events...")
    with open('../Events.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Get the event title/name
            name = row.get('Event Title', '')
            if not name:
                continue
                
            slug = slugify(name)
            
            # Check if the event already exists
            if Event.objects.filter(slug=slug).exists():
                print(f"Event '{name}' already exists. Skipping...")
                continue
            
            # Use an available location or create a default one
            if DiveLocation.objects.exists():
                location = DiveLocation.objects.first()