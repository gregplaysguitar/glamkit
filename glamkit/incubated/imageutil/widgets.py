from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.conf import settings
from django.utils.safestring import mark_safe

class ImageWithHighlightWidget(AdminFileWidget):
    """
    An image field widget that displays a preview together with a crop interface.
    Possible attrs are: ratio: integer (width/height), min_size: [min_x, min_y], max_size: [max_x, max_y]
    """
    def __init__(self, *args, **kwargs):
        super(ImageWithHighlightWidget, self).__init__(*args, **kwargs)
        self.attrs = kwargs.get('attrs', {})
        self.ratio = self.attrs.get('ratio', 0)
        self.min_size = self.attrs.get('min_size',[0,0])
        self.max_size = self.attrs.get('max_size', [0,0])
    
    def render(self, name, value, attrs=None):
        identifier = attrs.get('id','')
        html = super(ImageWithHighlightWidget, self).render(name, value, attrs)
        image_url = getattr(value, 'url', '')
        image_name = getattr(value, 'name', '')
        
        if self.ratio:
            ratio_rule = "aspectRatio: %s," % self.ratio
        else:
            ratio_rule = "aspectRatio: 0,"
        if self.min_size:
            min_size_rule = "minSize:[%s, %s]," % (self.min_size[0], self.min_size[1])
        else:
            min_size_rule = ""
        if self.max_size:
            max_size_rule = 'maxSize:[%s, %s],' % (self.max_size[0], self.max_size[1])
        else:
            max_size_rule = ""
        
        out = u"""<div class='clear'>
                    <script type='text/javascript'>
                        $(document).ready(function(){
                        var size_ratio = %(ratio)s;
                        var preview_height = 150;
                        if(size_ratio)
                            var preview_width = preview_height * size_ratio;
                        else
                            var preview_width = preview_height;
                        
                        $('#preview_%(identifier)s').parent().width(preview_width).height(preview_height);                      
                        previewFunc = generatePreviewFunc('%(identifier)s', preview_width, preview_height);
                        // check if values are already filled in to the dimension fields, and make the selection match
                        var selected_x = $('#%(identifier)s_highlight_x').val() == ""? 0 : $('#%(identifier)s_highlight_x').val();
                        var selected_y = $('#%(identifier)s_highlight_y').val() == ""? 0 : $('#%(identifier)s_highlight_y').val();
                        var selected_width = $('#%(identifier)s_highlight_width').val() == ""? preview_width : $('#%(identifier)s_highlight_width').val();
                        var selected_height = $('#%(identifier)s_highlight_height').val() == ""? preview_height : $('#%(identifier)s_highlight_height').val();

                        // Just to be sure it works if no values are supplied in the fields
                        $('#%(identifier)s_highlight_x').val(selected_x);
                        $('#%(identifier)s_highlight_y').val(selected_y);
                        $('#%(identifier)s_highlight_width').val(selected_width);
                        $('#%(identifier)s_highlight_height').val(selected_height);
                    
                        var select_rule = [parseInt(selected_x), parseInt(selected_y), parseInt(selected_x) + parseInt(selected_width), parseInt(selected_y) + parseInt(selected_height)]
                        $("#jcrop_target_%(identifier)s").Jcrop({
                            %(ratio_rule)s
                            %(min_size_rule)s
                            %(max_size_rule)s
                            onChange: previewFunc,
                            onSelect: previewFunc,
                            setSelect:select_rule
                        });
                        })
                    </script>
                    <img src='%(image_url)s' id='jcrop_target_%(identifier)s' alt='preview of %(image_name)s' class='preview_image' />
                    <div class='crop_preview' style='overflow:hidden;margin-left:5px;'>
                    <img src='%(image_url)s' id='preview_%(identifier)s' alt='crop preview of %(image_name)s' class='crop_preview_image' style='top:0;left:0;' />
                    </div>
                    <div class='white_bg'>%(html)s</div>
                    </div>
                """ % ({
                        'ratio_rule':ratio_rule, 
                        'min_size_rule':min_size_rule,
                        'max_size_rule':max_size_rule,
                        'ratio':self.ratio, 
                        'image_url':image_url, 
                        'identifier':identifier, 
                        'image_name':image_name, 
                        'html':html
                        })
        return mark_safe(out)
    
    class Media:
        js = (
            '%sjs/jquery.min.js' % settings.ADMIN_MEDIA_PREFIX,
            '%sjs/imagehighlight/utils.js' % settings.MEDIA_URL,
            '%sjs/imagehighlight/jquery.Jcrop.min.js' % settings.MEDIA_URL,
        )
        css = {
            'screen': (
                '%scss/imagehighlight/jquery.Jcrop.css' % settings.MEDIA_URL,
            )
        }