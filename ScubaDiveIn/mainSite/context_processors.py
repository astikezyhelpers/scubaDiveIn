import json
import os
from django.conf import settings

def schema_markup(request):
    """
    Context processor to add schema markup to all templates
    """
    # Load the schema markup file
    schema_file_path = os.path.join(settings.BASE_DIR, 'schema_markup.json')
    
    try:
        with open(schema_file_path, 'r', encoding='utf-8') as file:
            schema_data = json.load(file)
            
        # Convert to JSON string for template use
        schema_json = json.dumps(schema_data, ensure_ascii=False)
        
        return {
            'schema_markup': schema_json,
            'schema_data': schema_data
        }
    except FileNotFoundError:
        return {
            'schema_markup': '{}',
            'schema_data': {}
        }

def page_specific_schema(request):
    """
    Generate page-specific schema markup based on the current URL
    """
    current_url = request.path
    page_schema = {}
    
    # Course detail pages
    if '/courses/' in current_url and current_url != '/courses/':
        page_schema = {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": "Dynamic Course Name",  # Replace with actual course data
            "provider": {
                "@type": "Organization",
                "name": "ScubaDiveIn"
            }
        }
    
    # Blog detail pages
    elif '/blog/' in current_url and current_url != '/blogs/':
        page_schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "publisher": {
                "@type": "Organization",
                "name": "ScubaDiveIn"
            }
        }
    
    # Service detail pages
    elif '/service/' in current_url:
        page_schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "provider": {
                "@type": "Organization",
                "name": "ScubaDiveIn"
            }
        }
    
    return {
        'page_schema': json.dumps(page_schema) if page_schema else None
    } 