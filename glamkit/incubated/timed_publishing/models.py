"""
Model for timed publishing

"""

from django.db import models
from timed_publishing.manager import TimedPublishingManager
from timed_publishing.settings import *
from django.core.exceptions import ValidationError


class TimedPublishingMixin(models.Model):
    """
    - has a status field which can flag an item as 'draft', 'dummy', 'published', 'removed' or 'scheduled'.
    - relies on settings.SERVER_MODE to determine its behaviour
    """

    objects = TimedPublishingManager()
    
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS,
                                 help_text=u'Only entries with "published" status will be displayed publicly.')
    
    publish_start = models.DateTimeField(blank=True,null=True, help_text=u'If this is Scheduled, then a publish start and end date needs to be added')
    publish_end = models.DateTimeField(blank=True,null=True)
    
    class Meta:
        abstract = True

    def clean(self):
        """
        validation:
        if the status is scheduled, then you've got to have a publish start and and end date
        the end date must be on or after the start date.
        """
        
        if self.status is SCHEDULED_STATUS:
            # end date must same or after start date.
            if self.publish_end is not None and self.publish_start is not None and self.publish_end < self.publish_start:
                raise ValidationError("end date (%s) must be greater than (or the same as) start date (%s)." % (self.publish_end, self.publish_start))
        
            if self.publish_start is None:
                raise ValidationError("Sorry, there must be an start date.")