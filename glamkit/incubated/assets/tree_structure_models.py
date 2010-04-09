from django.db import models


class TreeNodeMixIn(models.Model):
    """
    Abstract class which should be inherited by a subclasses, should 
    they wish to have tree-ordering capabilities
    """
    parent = models.ForeignKey('self', blank=True, null=True, db_index=True)
    order = models.IntegerField(editable=False, help_text="indicates which position the article should appear in, relative to its siblings, lower means higher",\
        db_index=True)

    def save(self, *args, **kw):
        if self.order is None:
            self.order = (self.__class__.objects.filter(parent=self.parent).aggregate(models.Max('order'))['order__max'] or 0) + 1
        return super(TreeNodeMixIn, self).save(*args, **kw)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        """
        Check that there are no circular references to parent
        (eg we don't want A to be born from B which was born from C
        which was born from A)
        """
        original_parent = self.parent
        parent = self.parent
        while parent is not None:
            parent = parent.parent
            if parent is not None and parent.pk == original_parent.pk:
                raise ValidationError("Cyclic references to parent are not allowed")
    
    """HTML output for the jstree plugin"""
    def _html_meta(self):
        return {"node_id": self.pk, "node_title": self.pk}
        
    def _html_tag(self):
        """
        This method should be overwritten by subclasses to create
        appropriate html representation
        """
        return u"<li id='%(node_id)s' class='open'><a href='#'><ins>&nbsp;</ins>%(node_title)s</a>" % self._html_meta()
    
    def to_ul(self, insert_ul=True):
        """
        Convert the tree structure to HTML using unordered lists
        Uses _html_tag to create individual tags
        
        @returns: unicode
        """
        children = self.__class__.objects.filter(parent=self).order_by('order')
        childish_html = "" if not children else "<ul>" + u"".join([kid.to_ul(False) for kid in children]) + "</ul>"
        output = self._html_tag() + childish_html + "</li>"
        if insert_ul:
            output = "<ul>" + output + "</ul>"
        return output
        
    def to_li(self):
        # oh that template language which forbids .to_ul(False) calls...
        return self.to_ul(False)
        
    class Meta:
        ordering = ["parent", "order"]
        abstract = True