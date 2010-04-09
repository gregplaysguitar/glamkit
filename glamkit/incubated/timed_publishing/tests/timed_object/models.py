from timed_publishing.models import TimedPublishingMixin
from timed_publishing.manager import TimedPublishingManager

from django.db import models


class TimedObject(TimedPublishingMixin):
    objects = TimedPublishingManager()

    title = models.CharField(max_length=30)