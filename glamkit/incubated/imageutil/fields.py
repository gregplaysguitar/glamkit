from widgets import ImageWithHighlightWidget
from django import forms
"""
Code largely inspired by: http://blog.elsdoerfer.name/2008/01/08/fuzzydates-or-one-django-model-field-multiple-database-columns/
"""


class ImageWithHighlightFormField(forms.ImageField):
    """
    A form field to do the image with highlight thing
    """
    widget = ImageWithHighlightWidget

