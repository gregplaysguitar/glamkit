from django.utils.encoding import force_unicode
from django.forms.widgets import CheckboxInput, SelectMultiple, RadioFieldRenderer, RadioInput
from django.utils.safestring import mark_safe, SafeUnicode, SafeString
from django.utils.html import escape, conditional_escape
from django.template.loader import render_to_string
from django.forms.util import flatatt

class CustomRadioInput(RadioInput):
    def __unicode__(self):
        return self.tag()

class FloatedSelectMultiple(SelectMultiple):
    """
    Provides selection of items via checkboxes.

    When providing choices for this field, give the item as the second
    item in all choice tuples. For example, where you might have
    previously used::

        field.choices = [(item.id, item.name) for item in item_list]

    ...you should use::

        field.choices = [(item.id, item) for item in item_list]
    """
    def __init__(self, item_attrs, *args, **kwargs):
        """
        item_attrs
            Defines the attributes of each item which will be displayed
            as a column in each table row, in the order given.

            Any callable attributes specified will be called and have
            their return value used for display.

            All attribute values will be escaped unless if they were explicitely marked safe.
        """
        super(FloatedSelectMultiple, self).__init__(*args, **kwargs)
        self.item_attrs = item_attrs

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        
        items = []
        # list of dictionaries, contains:
        # extra_class, rendered_cb, content
        
        str_values = set([force_unicode(v) for v in value]) # Normalize to strings.
        for i, (option_value, item) in enumerate(self.choices):
            option_value = force_unicode(option_value)
            check_test = lambda value: value in str_values
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                
            final_attrs.update({'onClick': 'change_cb(this)'})
            cb = CheckboxInput(final_attrs, check_test)
            rendered_cb = cb.render(name, option_value)
            
            cb = {"extra_class": 'image_selected' if check_test(option_value) else ""}
            cb["rendered_cb"] = rendered_cb
            cb["content"] = create_content(item, self.item_attrs)
            
            items.append(cb)
        return render_to_string("assets/admin/hero_image.html", {"items": items})
        
        
def create_content(item, item_attrs):
    out = []
    for attr in item_attrs:
        if callable(getattr(item, attr)):
            content = getattr(item, attr)()
        else:
            content = getattr(item, attr)
        if not (isinstance(content, SafeUnicode) or isinstance(content, SafeString)):
            content = escape(content)
        out.append(unicode(content))
    return out