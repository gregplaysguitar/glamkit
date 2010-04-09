from django.utils.simplejson.decoder import JSONDecoder

from django.utils.safestring import mark_safe
from django.contrib import admin
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.conf.urls.defaults import patterns
from django.http import HttpResponseRedirect, Http404
from django.db.models import F

from django.conf import settings

j = JSONDecoder()
j.ensure_ascii = False
    
class TreeNodeAdminMixIn(admin.ModelAdmin):
    actions = ['run_tree_structure']
    
    def response_action(self, request, queryset):
        if request.POST.get("action", None) == 'run_tree_structure':
            return self.run_tree_structure(None, None, None)
        return super(TreeNodeAdmin, self).response_action(request, queryset)
    
    def run_tree_structure(self, modeladmin, request, queryset):
        return HttpResponseRedirect("tree_structure/")
    run_tree_structure.short_description = "Re-order"
    
    def get_urls(self):
        return patterns('',
            (r'^tree_structure/$', self.tree_structure)
        ) + super(TreeNodeAdminMixIn, self).get_urls()
            
    def tree_structure(self, request):
        if request.method == "GET":
            return render_to_response("assets/tree_structure.html",
                {"roots": self.model.objects.filter(parent=None).order_by('order'),
                 "media": mark_safe(self.media)},
                context_instance=RequestContext(request))
        else:
            try:
                if not 'cancel' in request.POST:
                    moved_nodes = j.decode(request.POST["moved_nodes"]) 
                    for descr in moved_nodes:
                        node = self.model.objects.get(pk=int(descr["node"]))
                        ref_node = self.model.objects.get(pk=int(descr["relative_to"]))
                        _rel = descr["rel"]
                        
                        if _rel == "inside":
                            node.parent = ref_node
                            node.order = None # so that TreeNode.save can catch and overwrite it
                        else:
                            node.parent = ref_node.parent
                            _qs = self.model.objects.filter(parent=ref_node.parent)
                            if _rel == "after":
                                _qs.filter(order__gt=ref_node.order).update(order=F('order')+1)
                                node.order = ref_node.order + 1
                            elif _rel == "before":
                                _qs.filter(order__lt=ref_node.order).update(order=F('order')-1)
                                node.order = ref_node.order - 1
                        # else should never happen. really.      
                        node.save()
            except (self.model.DoesNotExist, ValueError, IndexError):
                raise Http404("Invalid POST data - try going back and re-submitting the form")
                    
            return HttpResponseRedirect("../")
    
    class Media:
        js = ("%sjs/jquery.min.js" % settings.ADMIN_MEDIA_PREFIX,
              "%s/assets/js/external/json2.js" % settings.MEDIA_URL,
              "%s/assets/js/external/jstree/jquery.tree.js" % settings.MEDIA_URL)
    
