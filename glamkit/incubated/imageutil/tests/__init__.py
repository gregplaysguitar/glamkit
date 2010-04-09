from imageutil.tests.tools import ImageWithHighlightTestCase
from imageutil.tests.test_settings import TEST_UPLOAD_DIRECTORY
import random, os, shutil
from django.conf import settings
from django.core.files.images import ImageFile
from django.core.urlresolvers import reverse


class TestExtraFields(ImageWithHighlightTestCase):
    
    def check_model(self, owi):
        """
        Check that we can do everything we expect with a model instance
        """
        attrs = ['image_highlight_x',
                'image_highlight_y', 
                'image_highlight_width',
                'image_highlight_height',
                'other_image_highlight_x',
                'other_image_highlight_y', 
                'other_image_highlight_width',
                'other_image_highlight_height',]
        for att in attrs:
            # check the hidden fields are there
            attribute_value = getattr(owi, att, None)
            if attribute_value is not None:
                self.assertEquals(str(type(attribute_value)), "<type 'int'>" )
        
        for att in attrs:
            # check you can set all the fields
            setattr( owi, att, random.randint(0,50))
            owi.save()
        
        # check you can delete the item
        owi.delete()
        
    def test_model(self):
        from imageutil.tests.testapp.models import ObjectWithImage
        owi = ObjectWithImage.objects.all()[0]
        self.check_model(owi)
        new_owi = ObjectWithImage.objects.create()
        self.check_model(new_owi)
        
class TestTemplateTag(ImageWithHighlightTestCase):
    urls = 'imageutil.tests.testapp.test_urls'
    def test_template_tag(self):
        from imageutil.tests.testapp.models import ObjectWithImage
        directory_path = os.path.join(settings.MEDIA_ROOT, TEST_UPLOAD_DIRECTORY)
        # don't proceed if there's already a directory at the path, or we might end up deleting something...
        self.assertFalse(os.path.exists(directory_path))
        os.mkdir(directory_path)
        # copy the file into the path
        file_name = 'imageutil_test_upload.jpg'
        file_source = os.path.join(os.path.dirname(__file__),'uploadable_file', file_name)
        file_destination = os.path.join(directory_path, file_name)
        shutil.copy(file_source, file_destination)
        # actually do the tests
        # remove the owi that was created by the fixture
        ObjectWithImage.objects.all().delete()
        self.assertEquals(ObjectWithImage.objects.count(), 0)
        owi = ObjectWithImage.objects.create(
            name='a tester',
            image = file_destination,
            image_highlight_x=10,
            image_highlight_y=10,
            image_highlight_width=20,
            image_highlight_height=20,
            
            another_image = file_destination,
            another_image_highlight_x=12,
            another_image_highlight_y=12,
            another_image_highlight_width=10,
            another_image_highlight_height=10,
        )
        self.assertEquals(ObjectWithImage.objects.count(), 1)        
        #ping the test url to make sure it can create the crop
        url = reverse('testit')
        response = self.client.get(url)
        self.assertTrue("a2041490074.jpg" in str(response))
        self.assertTrue("a1746449152.jpg" in str(response))
        # (the url of the image is different each time we run the test because its modification date is different)
        # The last part of the URL is a hash of the resize arguments, which are constant
        try:
            from BeautifulSoup import BeautifulSoup
            soup = BeautifulSoup(str(response))
            image_url_1 = soup('img')[0]['src']
            image_url_2 = soup('img')[1]['src']
            # check that the image exists
            image_response_1 = self.client.get(image_url_1)            
            image_response_2 = self.client.get(image_url_2)            
            self.assertEquals(image_response_1.status_code, 200)
            self.assertEquals(image_response_2.status_code, 200)

            from PIL import Image as pil_image
            from StringIO import StringIO
            im_1 = pil_image.open(StringIO(image_response_1.content))
            im_2 = pil_image.open(StringIO(image_response_2.content))
            # check that it actually was cropped
            self.assertEquals(im_1.size, (20, 20))   
            self.assertEquals(im_2.size, (10, 10))   

            real_file_path = os.path.join(settings.MEDIA_ROOT, image_url_1[len(settings.MEDIA_URL):])
            shutil.rmtree(os.path.dirname(real_file_path))
        except ImportError:
            # don't worry too much if BeautifulSoup or PIL isn't there.
            pass
        
        # tidy up
        for file_name in os.listdir(directory_path):
            os.remove(os.path.join(directory_path,file_name))
        os.rmdir(directory_path)

