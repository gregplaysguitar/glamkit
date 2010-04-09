"""
A manager for the production site; only published or scheduled objects are returned.
"""

from django.db import models
from django.db.models import Q
import datetime
from django.conf import settings

from timed_publishing.settings import *

class TimedPublishingManager(models.Manager):

    def get_query_set(self):
        """
        if SERVER_MODE=="production" the custom manager will not display items marked as draft, dummy or removed
        """
        
        queryset = super(TimedPublishingManager, self).get_query_set()
        
        if settings.SERVER_STATUS == 'production':
            queryset = queryset.filter(Q(status=PUBLISHED_STATUS) | Q(status=SCHEDULED_STATUS))
        
        """
        if status == scheduled, the model relies on 2 additional datetime fields
        (publish_start and publish_end) to determine if the object should be displayed
        
        ie: exclude ones who are scheduled and whose publish_end has passed or publish_start has not arrived.
        a publish end may be null
        """
        
        queryset = queryset.exclude( 
                                        Q(status=SCHEDULED_STATUS) & 
                                        (
                                            (
                                                Q(publish_end__isnull=False) &
                                                (Q(publish_start__gte=datetime.datetime.now()) | Q(publish_end__lte=datetime.datetime.now()))
                                            ) |
                                            (
                                                Q(publish_start__gte=datetime.datetime.now()) & Q(publish_end__isnull=True)
                                            )
                                        )
                                   )
        
        return queryset