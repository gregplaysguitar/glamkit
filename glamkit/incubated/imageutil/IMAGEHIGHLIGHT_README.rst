IMAGEHIGHLIGHT - image highlight creator
----------------------------------------

Put the imagehighlight folders from each of the media/css media/js etc folders into your media/js etc folders

in your model do something like this:

from imageutil.model_fields import ImageWithHighlightField

>>> # In your model do something like this:
>>> class ObjectWithImage(models.Model):
>>>     name = models.CharField(max_length=50)
>>>     image = ImageWithHighlightField(upload_to='files/')
>>>     another_image = ImageWithHighlightField(upload_to='files/')
>>>     
>>>     def __unicode__(self):
>>>         return "%s saved at %s" % (self.name, self.image.url)

You can pass additional arguments to the ImageWithHighlightWidget- some or all of those shown here:
# my_image = ImageWithHighlightField(upload_to='files/', 
									widget=ImageWithHighlightWidget(
										attrs=
											{
											max_size: [20, 20],
											min_size: [10, 10],
											ratio: 1.414,
											}))
# .. where ratio is width/height

in your admin.py, do at least this

>>> from django.contrib import admin
>>> from models import ObjectWithImage

>>> admin.site.register(ObjectWithImage)


in your template do something like this:

{% load imagehighlight %}

{% highlight imagefield %}

This will crop the image to the image highlight.

{% highlight imagefield widthxheight %}

This will return a widthxheight image that contains the entire highlight region.