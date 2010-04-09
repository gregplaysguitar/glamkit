"""
A template filter which wraps imagemagick's `convert` command. The filter acts upon a source image path, and returns the filtered image path.
    
    usage: {{ source_path|convert:"-resize 64x64\!" }}
    
The filter parameter is the processing arguments for an ImageMagick 'convert' command. See e.g. http://www.imagemagick.org/Usage/resize/
    
Every image created is saved in a cache folder. This code does not handle removing obsolete cached images. If the filtered image path exists already, no image processing is carried out, and the path is returned.
    
"""

from django import template
from imageutil.imagemagick_util import convert as do_convert

register = template.Library()

@register.filter
def convert(original_image_path, arg=""):
    return do_convert(original_image_path, arg)
