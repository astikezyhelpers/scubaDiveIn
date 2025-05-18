from django.db import models
from django.core.files.uploadedfile import UploadedFile
from django.forms import FileField
from django.forms.widgets import FileInput
from django.core.exceptions import ValidationError
from .imagekit_config import upload_image, get_optimized_image_url

class ImageKitFormField(FileField):
    """
    Form field for ImageKit uploads
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = FileInput()
    
    def clean(self, value, initial=None):
        value = super().clean(value, initial)
        if value is None:
            return initial
        if not isinstance(value, UploadedFile):
            return value
        return value

class ImageKitField(models.Field):
    """
    Custom field for ImageKit integration
    """
    def __init__(self, folder_name=None, *args, **kwargs):
        self.folder_name = folder_name
        kwargs['max_length'] = kwargs.get('max_length', 500)
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def formfield(self, **kwargs):
        defaults = {'form_class': ImageKitFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return value

    def to_python(self, value):
        if value is None:
            return value
            
        if isinstance(value, UploadedFile):
            try:
                # Check file size (max 10MB)
                if value.size > 10 * 1024 * 1024:
                    raise ValidationError('Image file too large. Maximum size is 10MB.')
                
                # Check file type
                if not value.content_type.startswith('image/'):
                    raise ValidationError('Invalid file type. Please upload an image file.')
                
                # Upload to ImageKit and return the URL
                result = upload_image(value, self.folder_name)
                if result and isinstance(result, dict) and result.get('url'):
                    return result['url']
                
                print("Upload failed - result:", result)
                if result is None:
                    raise ValidationError('Failed to upload image. Please try again.')
                raise ValidationError('Failed to get URL from ImageKit. Please try again.')
            except ValidationError:
                raise
            except Exception as e:
                print(f"Upload exception: {str(e)}")
                raise ValidationError('Error uploading image. Please try again.')
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value) 