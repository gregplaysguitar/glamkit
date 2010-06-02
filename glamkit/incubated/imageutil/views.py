from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from imagemagick_util import convert
import os

IMAGEUTIL_SHORTCUTS = getattr(settings, "IMAGEUTIL_SHORTCUTS", {})


def image_convert(request, filepath):
    """
    Converts and saves an image according to spec in the GET parameters, and redirects to the result.
    
    takes urls of the form:
    
    /image_convert/path/to/image.jpg?resize=120x120^&strip&quality=50
    or
    /image_convert/path/to/image.jpg?-resize 120x120^ -gravity north -extent 120x120
    
    The difference between the two is that, despite appearences, order is NOT defined in the first example (in the example order doesn't matter), whereas order is defined in the second example (and it matters in the example given) - the GET string is passed directly to convert.
    
    path/to/image.jpg is a path to image relative to MEDIA_ROOT. 
    
    """
    
    import warnings
    warnings.warn("image_convert view is deprecated (it starts a new django instance to process the request, and causes cacheing/redirecting issues with interactive javascript apps). Use the |convert:\"params\" filter instead.\n")
    
    if len(request.GET)==1:
        a = request.GET.keys()[0]
        if a[0] == "-": #it's a one-liner
            url = convert(filepath, a)
        elif a in IMAGEUTIL_SHORTCUTS:
            url = convert(filepath, a)            
        else:
            url = convert(filepath, "-%s %s" % (a, request.GET[a]))
    else:
        arglist = " ".join(["-%s %s" % (arg, arg_value) for arg, arg_value in request.GET.items()])
        url = convert(filepath, arglist)
        
    return HttpResponseRedirect(url)