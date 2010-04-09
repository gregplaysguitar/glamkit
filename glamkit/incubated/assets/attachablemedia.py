from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

"""
Mixin that allows model instances to have a collection of visualmedia (interleaving images and videos)
"""

class OrderedMediaAttachment(models.Model):
    """
    An abstract m2m intermediary model which attaches pieces of VisualMedia to pieces of content, in the order determined by rank.
    
    Concrete subclasses should implement 'object' as a ForeignKeyField on the model to attach media to. E.g. if attaching to a blog post:
    
    class BlogMediaAttachment(OrderedMediaAttachment):
        object=models.ForeignKeyField(BlogPost)

    
    class BlogPost(models.Model):
        media = models.ManyToManyField(VisualMedia, through=BlogMediaAttachment)
        ...
    """
    media = models.ForeignKey("VisualMedia")
    rank  = models.FloatField(db_index=True, default=0, help_text="For deciding the order of the visualmedia. The higher the rank, the more prominent (or earlier) the media in the list.")

    class Meta:
        abstract = True
        ordering = ["-rank"]
        
class OrderedImageAttachment(models.Model):
    """
    Same as above, but restricted to images.
    
    Concrete subclasses should implement 'object' as a ForeignKeyField on the model to attach media to.
    """
    media = models.ForeignKey("Image")
    rank  = models.FloatField(db_index=True, default=0, help_text="For deciding the order of the image. The higher the rank, the more prominent (or earlier) the image in the list.")

    class Meta:
        abstract = True
        ordering = ["-rank"]

class OrderedVideoAttachment(models.Model):
    """
    Same as above, but restricted to videos.
    
    Concrete subclasses should implement 'object' as a ForeignKeyField on the model to attach media to.
    """
    media = models.ForeignKey("Video")
    rank  = models.FloatField(db_index=True, default=0, help_text="For deciding the order of the video. The higher the rank, the more prominent (or earlier) the video in the list.")

    class Meta:
        abstract = True
        ordering = ["-rank"]