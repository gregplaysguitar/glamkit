from django import forms

from django.conf import settings

from assets.widgets import force_unicode, create_content, CustomRadioInput, RadioFieldRenderer, render_to_string
from assets.models import Image

def generate_renderer(item_attrs):
    """
    Same item_attrs as in FloatedSelectMultiple
    
    We need a class factory because in this particular case there is no easy
    way to pass a particular parameter to the renderer
    """
    class RadioFloatedRenderer(RadioFieldRenderer):
        """
        Displays list in the same manner as FloatedSelectMultiple
        """
        custom_attrs = item_attrs
        
        def render(self):
            items = []
            value = [] if self.value is None else self.value
            str_values = set([force_unicode(v) for v in value])
            
            for i, (option_value, item) in enumerate(self.choices):
                option_value = force_unicode(option_value)
                check_test = lambda value: value in str_values
                cb = force_unicode(CustomRadioInput(self.name, self.value, self.attrs.copy(), (option_value, ""), i))
                
                items.append({"rendered_cb": cb, 
                              "content": create_content(item, self.custom_attrs),
                              "extra_class": 'image_selected' if check_test(option_value) else ""})

            return render_to_string("assets/hero_image.html", {"items": items})
                  
    return RadioFloatedRenderer
    

class HeroImageFormMixIn(object):
    def __init__(self, *args, **kw):
        if "hero_image" in self.fields: # it may have been deleted
            self.fields['hero_image'].choices = [(item.id, item) for item in Image.objects.all()]
        
class HeroImageAdminMixIn(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
        help_text = "If you add a new image by clicking the cross (on the left) you'll have to refresh this page to see the new image appear in the list above."
        if db_field.name == 'hero_image':
            db_field.help_text = help_text
            kwargs['widget'] = forms.widgets.RadioSelect(renderer=generate_renderer(['thumb', 'name']))
        return super(HeroImageAdminMixIn, self).formfield_for_dbfield(db_field, **kwargs)
        
    class Media:
        js = ("%sjs/jquery.min.js" % settings.ADMIN_MEDIA_PREFIX,
               "%sassets/js/external/jquery.form.js" % settings.MEDIA_URL)