from django.db import models
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from fields import ImageWithHighlightFormField
from widgets import ImageWithHighlightWidget

try:
    import imageutil
except ImportError:
    raise


_highlight_field_name = lambda name, value: "%s_highlight_%s" % (name, value)

class ImageWithHighlightFieldFile(ImageFieldFile):
    def __init__(self, image, field, name, highlight_x, highlight_y, highlight_width, highlight_height, **kwargs):
        self.highlight_x=highlight_x
        self.highlight_y=highlight_y
        self.highlight_width=highlight_width
        self.highlight_height=highlight_height
        super(ImageWithHighlightFieldFile, self).__init__(image, field, name)

class ImageWithHighlightField(models.ImageField):
    """
    A model field for an image with a selectable highlight area.
    """
    #TODO: unhighlighting the below produces strange error. Would like to expose crop dimensions from file...
    # attr_class = ImageWithHighlightFieldFile

    def __init__(self, verbose_name=None, name=None, highlight_x=None, highlight_y=None, highlight_width=None, highlight_height=None, widget=None, **kwargs):
        self.highlight_x = highlight_x
        self.highlight_y = highlight_y
        self.highlight_width = highlight_width
        self.highlight_height = highlight_height
        self.widget = widget or ImageWithHighlightWidget
        super(ImageWithHighlightField, self).__init__(verbose_name, name, **kwargs)
        
    def get_internal_type(self):
        return 'CharField'
        
    def formfield(self, **kwargs):
        # having to set widget isn't mentioned in the docs..
        defaults = {'form_class': ImageWithHighlightFormField,
                    'widget':self.widget}
        kwargs.update(defaults)
        return super(ImageWithHighlightField, self).formfield(**kwargs)
        
    def contribute_to_class(self, cls, name):
        """
        Add the four extra fields that define the highlight area
        """
        highlight_x = models.IntegerField(null=True, blank=True)
        highlight_y = models.IntegerField(null=True, blank=True)        
        highlight_width = models.IntegerField(null=True, blank=True)
        highlight_height = models.IntegerField(null=True, blank=True)
        
        cls.add_to_class(_highlight_field_name(name, 'x'), highlight_x)
        cls.add_to_class(_highlight_field_name(name, 'y'), highlight_y)
        cls.add_to_class(_highlight_field_name(name, 'width'), highlight_width)
        cls.add_to_class(_highlight_field_name(name, 'height'), highlight_height)
        
        highlight_x.creation_counter = self.creation_counter
        highlight_y.creation_counter = self.creation_counter
        highlight_width.creation_counter = self.creation_counter
        highlight_height.creation_counter = self.creation_counter
        
        super(ImageWithHighlightField, self).contribute_to_class(cls, name)
        # setattr(cls, self.name, ImageWithHighlightFieldCreator(self)) #uncommenting this stops showing the title

    # @property
    # def highlight(self):
    #     return self.highlight_x, self.highlight_y, self.highlight_width, self.highlight_height




def IMAGE_WITH_HIGHLIGHT_ADMIN(fieldname, section_title=None):
   """Returns a spec for presenting the fields in the admin box"""
   return (section_title, {'fields': (
       fieldname,
       _highlight_field_name(fieldname, 'x'),
       _highlight_field_name(fieldname, 'y'),
       _highlight_field_name(fieldname, 'width'),
       _highlight_field_name(fieldname, 'height'),
   )})
  
       
#class ImageWithHighlightFieldCreator(object):
#    def __init__(self, field):
#        self.field = field
#        self.highlight_x_name = _highlight_field_name(self.field.name, 'x')
#        self.highlight_y_name = _highlight_field_name(self.field.name, 'y')
#        self.highlight_width_name = _highlight_field_name(self.field.name, 'width')
#        self.highlight_height_name = _highlight_field_name(self.field.name, 'height')
#    
#    def __get__(self, obj, type=None):
#        if obj is None:
#            raise AttributeError('Can only be accessed via an instance')
#        image = obj.__dict__[self.field.name]
#        if image is None: 
#            return None
#        else:
#            return ImageWithHighlightFieldFile(
#                        obj, 
#                        self.field, 
#                        self.field.name, 
#                        highlight_x=getattr(obj, self.highlight_x_name),
#                        highlight_y=getattr(obj, self.highlight_y_name),
#                        highlight_width=getattr(obj, self.highlight_width_name),
#                        highlight_height=getattr(obj, self.highlight_height_name)
#                        )
#                        
#    def __set__(self, obj, value):
#        if isinstance(value, ImageWithHighlightFieldFile):
#            obj.__dict__[self.field.name] = value.image
#            setattr(obj, self.highlight_x_name, value.highlight_x)
#            setattr(obj, self.highlight_y_name, value.highlight_y)
#            setattr(obj, self.highlight_width_name, value.highlight_width)
#            setattr(obj, self.highlight_height_name, value.highlight_height)
#        else:
#            obj.__dict__[self.field.name] = self.field.to_python(value)
