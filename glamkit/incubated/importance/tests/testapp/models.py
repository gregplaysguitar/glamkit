import re

from django.db import models

from importance.utils import calculate_importance
        
        
@calculate_importance(spikes=("posted",), tenthlife=6, max_importance=1000, min_importance=10)
class Post(models.Model):
    content = models.TextField(max_length=500)
    importance = models.FloatField(editable=False, default=1000)
    posted = models.DateField()