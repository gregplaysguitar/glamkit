from django import forms
from django.contrib import admin
from django.shortcuts import get_object_or_404

from django.conf import settings

from models import VisualMedia

def m2m_related_mixin_factory(qs_name, through_model):
    class BaseVisualMediaAttachmentFormSet(forms.models.BaseInlineFormSet):
        # Base InlineFormSet does some vodoo which makes things work
        # everything will be broken in a horrible horrible way if we inherit 
        # from BaseModelFormSet instead
        media = forms.Media()
        
        def __init__(self, *args, **kwargs):
            self.query = VisualMedia.objects.all()
            super(BaseVisualMediaAttachmentFormSet, self).__init__(*args, **kwargs)
            
            if self.is_bound and self.is_valid():
                # if main form contains errors we need to render the forms user 
                # has entered into our formset
                self.entered_data = sorted(self.cleaned_data, key=lambda f: f['rank']) 
                
        def save(self):
            # remove existing attached media:            
            [p.delete() for p in getattr(self.instance, qs_name).all()]
            objects = []
            # that bit was unnecessary in toben, for some reason
            # i guess admin internals were changed since then
            for form in self.forms:
                objects.append(form.save(commit=False))
            if objects:
                object_id = objects[0].object.id
                for obj in objects:
                    obj.object_id = object_id
                    obj.save()
        
    
    VisualMediaAttachmentFormSet = forms.models.modelformset_factory(through_model, formset=BaseVisualMediaAttachmentFormSet, extra=0)

    class M2MAttachmentInline(admin.TabularInline):
        media = forms.Media()
        model = through_model
        formset = BaseVisualMediaAttachmentFormSet
        extra = 0
        template = "assets/m2m_sortable.html"  # includes needed js and css
        
    
    class VisualMediaAdminMixIn(object):        
        def construct_change_message(self, request, form, formsets):
            # we don't really care about the change message, do we?
            # potential TODO
            return u"Data was updated"
            
        def add_view(self, request, form_url='', extra_context=None):
            if extra_context is None:
                extra_context = {}
            extra_context["qs_name"] = qs_name
            return super(VisualMediaAdminMixIn, self).add_view(request, form_url,
                extra_context)
                    
        def change_view(self, request, object_id, extra_context=None):
            if extra_context is None:
                extra_context = {}
            extra_context["attachments"] = getattr(get_object_or_404(self.model, pk=object_id), qs_name).order_by('rank').all()
            extra_context["qs_name"] = qs_name
            return super(VisualMediaAdminMixIn, self).change_view(request, object_id,
                extra_context)
                
        class Media:
            js = ("%sjs/jquery.min.js" % settings.ADMIN_MEDIA_PREFIX,
                  "%sassets/js/external/jquery-ui.min.js" % settings.MEDIA_URL)
                
        inlines = (M2MAttachmentInline,)
            
    return VisualMediaAdminMixIn
