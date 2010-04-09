"""
TODO
* Define overwritable constants. SOME_SETTING = getattr(settings, "SOME_SETTING", "default value")
* Meta inheritance http://docs.djangoproject.com/en/dev/topics/db/models/#meta-inheritance

"""


import random, string
import mimetypes
import os

from imageutil.model_fields import ImageWithHighlightField


from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

from ixc_common.mixins import Inheritable

from attachablemedia import *
from tree_structure_models import TreeNodeMixIn

import settings as appsettings

CHARS = string.letters + string.digits
# Patch mimetypes w/ any extra types
mimetypes.types_map.update(appsettings.EXTRA_MIME_TYPES)

def get_path(instance, filename):
    """
    this handy directory creating function *would* be very clever
    to use to calculate the upload_to path.
    however, since directory listings are turned off anyway, it's not
    actually any more obfuscatory than just having a long secret in
    the uplaod_to path
    
    How about i keep it here anyway to warm my spirit in my
    twilight years?
    """
    dir = "file_library/" + string.join(random.sample(CHARS, 16), '') + string.join(random.sample(CHARS, 16), '')
    return "%s/%s" % (dir, name)
    
class AbstractFile(models.Model, Inheritable):
    """
    abstract base class.
    subclasses need to implement the "file" property
    TODO: implement an upload_to callable that eliminates this need so it's neater.
    TODO: refactor this out if it's a waste of time.
    """
    _name = models.CharField("friendly name", max_length=200,blank=True,null=True, help_text="If this isn't specified, the filename, minus the extension, is used.") 
    mime_type = models.CharField(max_length=150,blank=True,null=True)
    
    @property
    def name(self):
        if self._name and self._name != None:
            return self._name
        #return the filename, minus the extension and any trailing _ (for duplicates)
        return ".".join(os.path.split(self.file.name)[1].split(".")[:-1]).rstrip("_")
    
    def __unicode__(self):
        return self.get_leaf_object().name
        
    class Meta:
        ordering = ("_name",)
        abstract=True

    def save(self, *args, **kwargs):
        if self.file and not self.mime_type:
            self.mime_type = mimetypes.guess_type(self.file.path)[0]
        super(AbstractFile, self).save(*args, **kwargs)
       
    def extension(self):
        return self.file.path.split(".")[-1]
        
    @property
    def size(self):
        return self.file.size
    
    @property
    def url(self):
        return self.file.url
        
    def link(self):
        return '<a href="%s">%s</a>' % (self.file.url, self.name)
    link.allow_tags = True
    link.short_description = 'Link'
    
    def as_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "mime_type": self.mime_type,
        }
        


        
class File(AbstractFile):
    """
        Any old file
    """
    file = models.FileField(upload_to=os.path.join(appsettings.ASSETS_PATH,"file/%Y/%m/%d/"), max_length=200)
    publish_date = models.DateField(db_index=True, help_text="This content won't be published until the publish date is reached.  Make it blank to unpublish.")
    
    class Meta:
        verbose_name = "document"
        verbose_name_plural = "documents"
        ordering = ['publish_date', '_name', 'file']
        
class VisualMedia(AbstractFile):
    """
        NON-Abstract base class for images and videos (so we can treat them as one).
        Subclasses need to implement an 'image' property, which is an ImageField, that we can get a 'width' and 'height' from. 'image' needn't contain anything for the purposes of this class.
    """
    
    def as_dict(self):
        s = super(VisualMedia, self).as_dict()
        s.update({'width': self.width, 'height': self.height})
        return s
    
    def thumb(self, template='assets/linked_thumbnail.html'):
        if self.image:
            return mark_safe(render_to_string(template, {
                'image': self.image
            }))
        return None
    thumb.allow_tags = True
    thumb.short_description = 'Thumbnail'
    
    def highlight_thumb(self, template='assets/highlight_thumbnail.html'):
        if self.image:
            return mark_safe(render_to_string(template, {
                'image': self.image
            }))
        return None
    highlight_thumb.allow_tags = True
    highlight_thumb.short_description = 'Highlight'

    def just_thumb(self):
        return self.thumb(template='assets/thumbnail.html')
    just_thumb.allow_tags = True
    just_thumb.short_description = 'Thumbnail'

    def dimensions_text(self):
        return "%d x %dpx" % (self.width, self.height)
    dimensions_text.short_description = 'Dimension'
    
    def aspect_ratio(self):
        return self.width*1.0/self.height
    aspect_ratio.short_description = 'Aspect Ratio'
    
    
class Image(VisualMedia):
    # In this case the 'image' is the same as the 'file' (satisfying AbstractFile and VisualMedia)
    file = ImageWithHighlightField("Image File",
        upload_to=os.path.join(appsettings.ASSETS_PATH, "images/%Y/%m/%d/"), max_length=200, width_field="width", height_field="height")
    _alt_text = models.TextField("Alt Text", blank=True, null=True, help_text="Use text that describes the image, or any text contained in it. If left blank, the 'Name' field is used.")
    width = models.IntegerField("Image Width")
    height = models.IntegerField("Image Height")

    def get_image(self):
        return self.file

    def set_image(self, image):
        self.file = image
        
    image = property(get_image, set_image)
    
    @property
    def alt_text(self):
        if self._alt_text:
            return self._alt_text
        return self.name
      
    def thumb(self, template='assets/highlight_thumbnail.html'):
        return mark_safe(render_to_string('assets/linked_thumbnail.html', {
            'MEDIA_URL': settings.MEDIA_URL,
            'url': self.file.url,
            'image_file': self.file.name,
        }))
    thumb.allow_tags = True
    thumb.short_description = 'Thumbnail'
            
    class Meta:
        ordering = ['_name', 'file']

            
class Video(VisualMedia):
    # In this case the 'image' is NOT the same as the 'file'
    file = models.FileField("Video File",
      upload_to=os.path.join(appsettings.ASSETS_PATH, "video/%Y/%m/%d/"), max_length=200, help_text="flv or mp4 files only")
    image = ImageWithHighlightField("Highlight Frame",
      upload_to=os.path.join(appsettings.ASSETS_PATH, "video/%Y/%m/%d/still_image/"), max_length=200, help_text="choose an optional still image to show for the video", blank=True, null=True, width_field="iwidth", height_field="iheight")

    vwidth = models.IntegerField("Video Width", blank=True, null=True, help_text="If blank, the highlight frame width will be used, or a global default will be used if no highlight frame is given.")
    vheight = models.IntegerField("Video Height", blank=True, null=True, help_text="If blank, the highlight frame height will be used, or a global default will be used if no highlight frame is given.")
    iwidth = models.IntegerField("Image Width", blank=True, null=True)
    iheight = models.IntegerField("Image Height", blank=True, null=True)
    
    @property
    def width(self):
        if self.vwidth:
            return self.vwidth
        elif self.iwidth:
            return self.iwidth
        else:
            return appsettings.DEFAULT_VIDEO_WIDTH
    
    @property
    def height(self):
        if self.vheight:
            return self.vheight
        elif self.iheight:
            return self.iheight
        else:
            return appsettings.DEFAULT_VIDEO_HEIGHT
    
    @property
    def player_height(self):
        return self.height + appsettings.VIDEO_CONTROLS_HEIGHT
    
    def as_dict(self):
        s = super(Video, self).as_dict()
        if(self.image):
            s.update({'highlight': self.image.url})
        return s