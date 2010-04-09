(I don't know .rst format. Anyone familiar with it - please format the document properly)

IxC assets
==========

... (description of VisualMedia and stuff)

Along with that, this library provides potentialy very useful admin mixins.

GENERAL NOTE:
I don't think there exists a convenient way for a mixin to alter the inheriting class media definition or inline definition.
So for now - if admin class is inheriting from inlines A, B and C you'll have to 
a) Add their inlines - inlines = (...my inlines...) + A.inlines + B.inlines + C.inlines
b) Add their js media definitions:
    class Media:
        js = (..my js...) + A.Media.js + B.Media.js + C.Media.js
        
    django media framework should take care of removing unneeded javascripts
c) If including jQuery do _not_ use the google one. If you don't want mixins to break, use django-included one - admin-media/js/jquery.min.js
    (this is subject to change)

1. Hero Image mixin
-------------------

Functionality:
    Provides a pretty selector for the hero image for the model.
    
Usage:
    a) The model must have a foreign key called hero_image pointing to assets.models.Image
    b) Import - from assets.hero_image_admin import HeroImageFormMixIn, HeroImageAdminMixIn
    c) Add HeroImageAdminMixIn to a list of iherited classes (the admin class will still need to inherit
        from admin.ModelAdmin). Make sure the custom form is provided.
    d) Add HeroImageFormMixIn to the list of parents in the form mentioned above. Once again,
        you'll still need to inherit from forms.ModelForm.
        You'll need to explicitly call __init__ method of mixin:
            class GenericContentForm(forms.ModelForm, HeroImageFormMixIn):
                def __init__(self, *args, **kw):
                    super(GenericContentForm, self).__init__(*args, **kw)
                    HeroImageFormMixIn.__init__(self, *args, **kw)
    
    
2. Selector for ordered related visual media mixin
--------------------------------------------------

Functionality:
    Provides a pretty drag-n-drop selector for related visual media. Related visual media has to be assets.models.VisualMedia
    
Usage:
    a) The model must have m2m relation to assets.models.VisualMedia, through a custom table which inherits from 
        assets.models.OrderedMediaAttachment
    b) Mixin must be created first through a class factory:
        from assets.m2m_related_admin import m2m_related_mixin_factory
        
        M2MRelated = m2m_related_mixin_factory(qs_name="genericmediaattachment_set", through_model=GenericMediaAttachment)
        
        where 'through_model' is a custom model through which m2m relation is defined
        and qs_name is a name which is used to get the related manager (usually it is name of the through_model,
        all lowercased + "_set"
        
    c) Inherit from the said mixin
    
    
3. Mixin for visual drag-n-drop tree ordering of the items through model
------------------------------------------------------------------------

Functionality:
    Name is self-descriptive. Currently it is done through the custom view added to the admin. It is accessible through actions in admin
    ("re order")
    
Usage:
    a) Inherit your model from assets.models.TreeNodeMixIn
    b) Create an _html_meta method in the model - 
    
    def _html_meta(self):
        """
        This method should be rewritten by subclasses to create
        appropriate html representation
        """
        return {"node_id": "%s" % self.pk, "node_title": self.title}
        
    node_title should be the string representing the node in the tree structure. Node_id should pretty much always be self.pk
    
    c) Inherit admin from TreeNodeAdminMixIn
    
    
