from .imagekit_config import imagekit

def test_imagekit_connection():
    """
    Test ImageKit connection and credentials
    """
    try:
        # Test URL generation
        url = imagekit.url({
            "path": "/test/sample.jpg",
            "transformation": [{"height": "300", "width": "400"}]
        })
        print("URL generation successful:", url)
        
        return True
    except Exception as e:
        print("ImageKit connection test failed:", str(e))
        return False 