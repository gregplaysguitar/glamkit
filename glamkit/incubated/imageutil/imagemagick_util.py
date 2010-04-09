from django.conf import settings
from django.http import Http404

import os
import shutil
import time
import re
import urlparse
import urllib
from subprocess import call

from exceptions import ImageMagickException, ImageMagickConversionError, ImageMagickOSFileError
from cache_util import file_hash

from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile

#Settings
ALLOWED_PARAMS = getattr(settings, "ALLOWED_PARAMS", "adaptive-resize resize extent gravity strip thumbnail trim quality crop liquid-rescale scale rotate shave unsharp watermark".split())
ERROR_IMAGE_URL = getattr(settings, 'ERROR_IMAGE_URL', '')
IMAGEUTIL_CACHE_PATH = getattr(settings, "IMAGEUTIL_CACHE_PATH", "imageutil_cache/")
IMAGEMAGICK_CONVERT_PATH = getattr(settings, 'IMAGEMAGICK_CONVERT_PATH', 'convert')
IMAGEUTIL_SHORTCUTS = getattr(settings, "IMAGEUTIL_SHORTCUTS", {})

#If an image takes more than 5secs or 10mb of memory, IM will quit.
IMAGEMAGICK_ALWAYS_PASS = getattr(settings, "IMAGEMAGICK_ALWAYS_PASS", "-limit area 10mb") # -limit time 5")

#no settings
_IMAGEUTIL_CACHE_ROOT = os.path.join(settings.MEDIA_ROOT, IMAGEUTIL_CACHE_PATH)
def convert(original_image_path, arg):
    """
    Takes the file name (relative to MEDIA_ROOT), and a specification of the conversion.
    
    Returns a URL to retrieve the converted file.
    
    See http://www.imagemagick.org/script/command-line-options.php for the possible options.

    Does the conversion, if it's not cached, and caches it in MEDIA_ROOT/IMAGEUTIL_CACHE.

    Pseudocode for filter:

    1. generate the result filename.
    2. does it exist? Yes = return it. No = create it.
    3. do the conversion; save the file as the result filename.
    
    @accepts:
    original_image_path - string - filename of the image; if the file specified lives outside MEDIA_ROOT ImageMagickException will be raised
    arg - string - list of arguments. all arguments must be included in ALLOWED_PARAMS, otherwise, ImageMagickException will be raised
    @returns:
    string - image url
    """
    try:
        # check that all arguments are in ALLOWED_PARAMS
        # we are assuming that all of the params that actually determine action start with dash
        panic = [a for a in arg.split() if (a.startswith("-") and not a[1:] in ALLOWED_PARAMS)]
        if panic:
            raise ImageMagickException("One of the arguments is not in a whitelist. List of arguments supplied: %s" % panic)
        arg = IMAGEUTIL_SHORTCUTS.get(arg, arg)
        
        if not original_image_path:
            raise ImageMagickOSFileError('No file specified')
        
        if isinstance(original_image_path, ImageField):
            original_image_path = original_image_path.path
            
        if isinstance(original_image_path, ImageFieldFile):
            original_image_path = original_image_path.path
        
        if not (isinstance(original_image_path, str) or isinstance(original_image_path, unicode)):
            raise ImageMagickException('Original image path is a %s, but it must be a string or unicode.' % str(type(original_image_path)))            
    
        op = os.path.abspath(os.path.join(settings.MEDIA_ROOT, original_image_path))
        if not op.startswith(os.path.normpath(settings.MEDIA_ROOT)): # someone's trying to access an image outsite MEDIA_ROOT; good luck with that!
            raise ImageMagickException("Image not under media root")
    
        if arg == "":
            #no processing to do.
            return urllib.quote(urlparse.urljoin(settings.MEDIA_URL,os.path.relpath(op, settings.MEDIA_ROOT)))

        #generate the cache filename
        try:
            #this depends on the file existing, so we needn't check elsewhere
            ophash = file_hash(op)
        except OSError, exc:
            raise ImageMagickOSFileError(*exc.args)

        try:
            foldername, filename = op.rsplit(os.path.sep, 1)
        except ValueError:
            foldername, filename = '', op        
        
        try:
            name, extension = filename.rsplit(".", 1)
        except ValueError:
            raise ImageMagickException("Filename does not include extension")
        
        arg_hash = hash(arg)
    
        destination_filename = "o%sa%s.%s" % (ophash, arg_hash, extension)
        
        rel_destination_folder = os.path.join(IMAGEUTIL_CACHE_PATH, filename)
        abs_destination_folder = os.path.join(_IMAGEUTIL_CACHE_ROOT, filename)
    
        rel_destination_file = os.path.join(rel_destination_folder, destination_filename)
        abs_destination_file = os.path.join(abs_destination_folder, destination_filename)

        url = urllib.quote(urlparse.urljoin(settings.MEDIA_URL, rel_destination_file))
        #is it in the cache? then return it
        if os.path.exists(abs_destination_file):
            os.utime(abs_destination_file, None) #update the modified timestamp (for cache purposes)
            return url
    
        if not os.path.exists(abs_destination_folder):
            os.makedirs(abs_destination_folder)
        
        # make sure that all supplied arguments are in the whitelist
        arg = re.sub("\s+", " ", IMAGEMAGICK_ALWAYS_PASS + " " + arg).strip() #having empty args in seems to break 'convert'
        
        arglist = [IMAGEMAGICK_CONVERT_PATH, op,] + arg.split(' ') + [abs_destination_file,]
        
        try:
            status = call(arglist)
        except OSError:
            raise OSError, "Check if your IMAGEMAGICK_CONVERT_PATH is correct. It is currently set to %s" % IMAGEMAGICK_CONVERT_PATH
            
        if status == 0:
            return url
        else:
            cmd = ' '.join(arglist)
            raise ImageMagickException, "Error converting %s: ImageMagick returned status %s (command was '%s')" % (op, status, cmd)
        
    except ImageMagickException, e:
        # something went wrong. return a filler image or nothing.
        # TODO - log, or process the error somehow.
        if settings.DEBUG:
            raise e
        else:
            return urllib.quote(ERROR_IMAGE_URL)
        
def tidy_cache(age=60*60*24*7): #1 week
    """
    Walks settings.IMAGE_CACHE_ROOT, deleting all files with a last modified date of more than `age` seconds ago.
    """
    cutoff = time.time()-age #num secs since epoch
    
    for path, folders, files in os.walk(_IMAGEUTIL_CACHE_ROOT):
        for f in files:
            fullpath = os.path.join(path,f)
            if os.path.getmtime(fullpath) < cutoff:
                os.remove(fullpath)