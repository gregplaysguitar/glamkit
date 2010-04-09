Imageutil Django app
Greg Turner, the Interaction Consortium

This application is for processing images with ImageMagick's 'convert' tool. The results are cached in the IMAGEUTIL_CACHE_PATH, and the client is redirected to the cached version of the file.


IMAGEMAGICK VERSION NOTE
------------------------
imageutil will work, in principle, with any version of ImageMagick. By default it will use one on the path. HOWEVER, several apps may use features only found in recent versions (6.3.8 has several useful resizing options, for example), so it is usually best to use a recent version.

Webfaction, for example, supplies IM at version 6.2.8, so it is usually necessary to install a newer version in your home directory. See http://forum.webfaction.com/viewtopic.php?id=1747 for installation instructions (only step 2, maybe 3 is necessary). Then add IMAGEMAGICK_CONVERT_PATH in settings to point to the newly-installed convert program.

INSTALLATION
------------

Install the application by adding 'imageutil' to your INSTALLED_APPS, and add a line to urls.py:

   url(r'^image_convert/', include('imageutil.urls')),

The default IMAGEUTIL_CACHE_PATH is "imageutil_cache/", and is relative to MEDIA_ROOT (since it's quickest to serve cached images without Django).

If you need to specify the path of 'convert' (ie if you have installed convert somewhere not on the path), add IMAGEMAGICK_CONVERT_PATH to settings (include the 'convert' filename).


TEMPLATE TAG
------------

Include {% load imagmagick %} in your templates. This turns on a 'convert' filter, which acts upon an image file path, and returns a URL to the converted image, like this (in this example, 'image' is also an ImageField):

<img src='{{ image.name|convert:"-resize 120 -strip -quality 50"}}' />

URL
---

You can call a URL which processes the image and redirects to the result like this:
    
    /image_convert/path/to/image.jpg?resize=120x120^&strip&quality=50

or this:

    /image_convert/path/to/image.jpg?-resize 120x120^ -gravity north -extent 120x120
  
The difference between the two is that, despite appearances, order is NOT defined in the first example (for this process order doesn't matter), whereas order IS defined in the second example (and it matters in the example given) - the GET string is passed directly to convert.

'path/to/image.jpg' is a path to the source image, relative to MEDIA_ROOT.

You can use this in templates like this (in this example, 'image' is an ImageField):

<img src='{% url image_convert image.name %}?resize=120&amp;strip&amp;quality=50' />

SHORTCUTS
---------

You can define shortcuts to image processing specs in settings.IMAGEUTIL_SHORTCUTS. For example, if

IMAGEUTIL_SHORTCUTS = {
    'area40000': "-resize 40000@ -strip -quality 60",
}

then visiting the URL
/image_convert/path/to/image.jpg?area40000
is the same as visiting
/image_convert/path/to/image.jpg?-resize+40000@+-strip+-quality+60

This makes including the same convert processing in several templates DRYer.


