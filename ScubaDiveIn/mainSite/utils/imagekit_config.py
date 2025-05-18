from imagekitio import ImageKit
from django.conf import settings
import os
import base64
import re
from django.utils.text import slugify
from datetime import datetime
from django.core.files.base import ContentFile
import io
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

imagekit = ImageKit(
    public_key=settings.IMAGEKIT_PUBLIC_KEY,
    private_key=settings.IMAGEKIT_PRIVATE_KEY,
    url_endpoint=settings.IMAGEKIT_URL_ENDPOINT
)

def sanitize_filename(filename):
    """
    Sanitize filename by:
    1. Converting spaces to hyphens
    2. Removing special characters
    3. Converting to lowercase
    4. Adding timestamp to ensure uniqueness
    """
    # Get the name and extension separately
    name, ext = os.path.splitext(filename)
    
    # Clean the name using slugify (converts spaces to hyphens, removes special chars)
    clean_name = slugify(name)
    
    # Add timestamp for uniqueness
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Combine everything back together
    return f"{clean_name}_{timestamp}{ext.lower()}"

def get_optimized_image_url(image_path, transformation_type='thumbnail'):
    """
    Get optimized image URL from ImageKit
    """
    if not image_path:
        return None
        
    transformations = {
        'thumbnail': [{'height': 300, 'width': 400}],
        'featured': [{'height': 800, 'width': 1200}],
        'gallery': [{'height': 600, 'width': 800}]
    }
    
    try:
        url = imagekit.url({
            "path": image_path,
            "transformation": transformations.get(transformation_type, [])
        })
        return url
    except Exception as e:
        print(f"ImageKit URL generation error: {str(e)}")
        return None

def upload_image(file, folder_name):
    """
    Upload image to ImageKit
    """
    try:
        # Read file content and convert to base64
        file_content = file.read()
        file.seek(0)  # Reset file pointer
        base64_file = base64.b64encode(file_content).decode('utf-8')
        
        # Sanitize the filename
        clean_filename = sanitize_filename(file.name)
        
        print(f"Uploading file with name: {folder_name}/{clean_filename}")  # Debug print
        print(f"File size: {len(file_content)} bytes")  # Debug print
        
        # Upload using ImageKit's upload method with base64 data
        try:
            # Create upload options using UploadFileRequestOptions
            options = UploadFileRequestOptions(
                use_unique_file_name=True,
                folder=f"/{folder_name}/"
                # Add other options here if needed, e.g., tags, is_private_file
            )
            
            # Perform the upload
            upload_response = imagekit.upload_file(
                file=base64_file,
                file_name=clean_filename,
                options=options  # Pass the options object
            )
            
            print("Raw upload response:", upload_response)  # Debug print
            
            # Check if upload_response is None
            if upload_response is None:
                print("Upload response is None")
                return None
                
            # Get the URL from the response
            url = upload_response.url if hasattr(upload_response, 'url') else None
            
            if url:
                print(f"Successfully uploaded image. URL: {url}")
                return {
                    'url': url,
                    'file_id': upload_response.file_id if hasattr(upload_response, 'file_id') else None,
                    'name': upload_response.name if hasattr(upload_response, 'name') else clean_filename
                }
            else:
                print("Upload successful but URL not found in response")
                print("Full response:", upload_response)
                return None
            
        except Exception as upload_error:
            print(f"ImageKit upload specific error: {str(upload_error)}")
            print(f"Error type: {type(upload_error)}")
            if hasattr(upload_error, 'response'):
                print(f"Error response: {upload_error.response}")
            return None
            
    except Exception as e:
        print(f"General error during upload: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"File info - name: {file.name}, size: {file.size if hasattr(file, 'size') else 'N/A'}, content_type: {file.content_type if hasattr(file, 'content_type') else 'N/A'}")
        return None 