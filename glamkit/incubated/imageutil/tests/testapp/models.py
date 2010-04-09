from django.db import models
from imageutil.model_fields import ImageWithHighlightField
import tempfile, os
from imageutil.tests.test_settings import TEST_UPLOAD_DIRECTORY
from django.conf import settings
tempdir = tempfile.gettempdir()

def get_test_upload_directory(instance, filename):
    return os.path.join(settings.MEDIA_ROOT,TEST_UPLOAD_DIRECTORY, filename) 

# A test model for the above
class ObjectWithImage(models.Model):
    name = models.CharField(max_length=50)
    image = ImageWithHighlightField(upload_to=get_test_upload_directory)
    another_image = ImageWithHighlightField(upload_to=get_test_upload_directory)
    
    def __unicode__(self):
        return "%s saved at %s" % (self.name, self.image.url)
        
        
