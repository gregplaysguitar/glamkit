from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import Image as PILImage
from assets.models import Image as AssetsImage
from django.core.files import File

class Command(BaseCommand):
    help = """Makes an Image asset for every Image in a given folder and its subfolders.

    Argument: folder (required) - the parent folder of images to upload.
    
    The images will be 'uploaded' in the normal way, so running the command twice will result in duplicates. 
    """
    requires_model_validation = False

    def handle(self, *args, **options):
        
        for root, dirs, files in os.walk(args[0]):
            for fn in files:
                path = os.path.join(root, fn)
                try:
                    PILImage.open(path)

                    f = File(open(path))
                    i = AssetsImage(file=f)
                    i.save()
                    
                    print "imported %s" % path
                    
                except IOError:
                    pass #not an image
                
        return "Images Imported"