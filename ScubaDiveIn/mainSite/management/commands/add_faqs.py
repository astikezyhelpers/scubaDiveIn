from django.core.management.base import BaseCommand
from mainSite.models import FAQ

class Command(BaseCommand):
    help = 'Adds FAQs from the document'

    def handle(self, *args, **kwargs):
        faqs_data = [
            {
                'question': 'What is scuba diving?',
                'answer': 'Scuba diving is a form of underwater diving where divers use breathing equipment (scuba gear) that is completely independent of a surface air supply. This allows divers to stay underwater longer and explore marine environments.',
                'category': 'General',
                'order': 1
            },
            {
                'question': 'Do I need to know how to swim to scuba dive?',
                'answer': 'Yes, basic swimming ability is required for scuba diving. You should be able to swim 200 meters without any swimming aids and float/tread water for 10 minutes.',
                'category': 'Prerequisites',
                'order': 2
            },
            {
                'question': 'What is the minimum age requirement for scuba diving?',
                'answer': 'The minimum age for scuba diving varies by certification level. For Discover Scuba Diving (DSD) experiences, the minimum age is typically 10 years. For full certification courses, the minimum age is usually 12 years.',
                'category': 'Prerequisites',
                'order': 3
            },
            {
                'question': 'What medical conditions might prevent me from diving?',
                'answer': 'Several medical conditions may affect your ability to dive safely, including heart conditions, lung diseases, ear problems, and pregnancy. A medical evaluation is required before diving, and you should consult with a diving medical professional.',
                'category': 'Health & Safety',
                'order': 4
            },
            {
                'question': 'What equipment do I need for scuba diving?',
                'answer': 'Essential scuba equipment includes a mask, fins, wetsuit, BCD (Buoyancy Control Device), regulator, air tank, depth gauge, and dive computer. For training courses and DSD experiences, all equipment is typically provided.',
                'category': 'Equipment',
                'order': 5
            },
            {
                'question': 'How long does a scuba diving course take?',
                'answer': 'Course duration varies by level. A Discover Scuba Diving experience takes about half a day. The basic Open Water certification typically takes 3-4 days, including classroom sessions, pool training, and open water dives.',
                'category': 'Courses',
                'order': 6
            },
            {
                'question': 'Is scuba diving dangerous?',
                'answer': 'When proper safety protocols are followed and you dive within your training limits, scuba diving is a relatively safe activity. Risks are minimized through proper training, equipment maintenance, and following diving guidelines.',
                'category': 'Health & Safety',
                'order': 7
            },
            {
                'question': 'What is the best time to dive in Andaman?',
                'answer': 'The best diving season in Andaman is from October to May, with peak conditions between December and April. The water is clearest during these months with visibility ranging from 20-40 meters.',
                'category': 'Location Specific',
                'order': 8
            },
            {
                'question': 'What marine life can I expect to see?',
                'answer': 'Andaman waters host diverse marine life including colorful coral reefs, tropical fish, manta rays, reef sharks, sea turtles, and occasionally dugongs. The specific marine life varies by dive site and season.',
                'category': 'Location Specific',
                'order': 9
            },
            {
                'question': 'What is your cancellation policy?',
                'answer': 'Cancellations made 48 hours or more before the scheduled activity receive a full refund. Cancellations within 24-48 hours receive a 50% refund. No refunds are given for cancellations less than 24 hours before the activity.',
                'category': 'Booking & Policies',
                'order': 10
            }
        ]

        for faq_data in faqs_data:
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults={
                    'answer': faq_data['answer'],
                    'category': faq_data['category'],
                    'order': faq_data['order']
                }
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added FAQ: {faq_data["question"][:50]}...')
            ) 