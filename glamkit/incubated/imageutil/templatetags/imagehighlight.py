"""
A template tag to automatically crop an image_with_highlight to show just the highlight

{% highlight name_of_image_with_highlight_field resize_spec %}
returns the path of the cropped image relative to media_root, so you'd use it like this:
<img src='{% resize my_object.image_field widthxheight %}' alt='a highlighted image' />
"""
from django import template
from imageutil.imagemagick_util import convert as convert_util
register = template.Library()
import re
from imageutil.exceptions import ImageMagickOSFileError

dim_re = re.compile(r'(\d+)x(\d+)')

@register.tag
def highlight(parser, token):
    # split_contents() knows not to split quoted strings.
    args = token.split_contents()
    if len(args)==2:
        tag_name, image_field = args
        target_dims = None
    elif len(args)==3:
        tag_name, image_field, target_dims = args
    else:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]        
    return HighlightResizeNode(image_field, target_dims)

class HighlightResizeNode(template.Node):
    def __init__(self, image_field, target_dims=None):
        
        self.model_object = template.Variable(image_field)
        if target_dims:
            self.target_dims = template.Variable(target_dims)
        else:
            self.target_dims = None
        
            
    def centred_crop(self, total_size, highlight_start, highlight_size, crop_size, cap_to_highlight=True):
        """returns (crop start, crop_size), being the coordinates at which to start and measure cropping such that the highlight is as central as possible within the crop.
        
        If cap_to_highlight, then the returned crop will be enlarged to match the highlight.
        """
        
        # if crop_size > total_size:
            # crop_size = total_size
              
        #figure out the 'ideal' crop, centered on the highlight.
        highlight_centre = highlight_start + highlight_size/2.0
        ideal_crop = [highlight_centre - crop_size/2, highlight_centre + crop_size/2]
             
        #if cap_to_highlight, enlarge the ideal crop to be the size of the higlight (and return
        if cap_to_highlight:
            if (ideal_crop[1]-ideal_crop[0]) < highlight_size:
                return (highlight_start, highlight_size)
      
        #if the bounds of ideal_crop fall outside of the total size, shift the bounds so that both bounds fall inside.
        if ideal_crop[0] < 0:
            ideal_crop[1] = ideal_crop[1]-ideal_crop[0]
            ideal_crop[0] = 0
        elif ideal_crop[1] > (total_size-1):
            ideal_crop[0] = ideal_crop[0] + ideal_crop[1] - total_size
            ideal_crop[1] = total_size
        #done.
        
        return (int(ideal_crop[0]), int(ideal_crop[1]-ideal_crop[0]))
        
        
    def render(self, context):
        target_width = target_height = None
        if self.target_dims:
            actual_target_dims = self.target_dims.resolve(context)
            target_width, target_height = dim_re.match(actual_target_dims).groups()
        if target_width:
            self.target_width = int(target_width)
        else:
            self.target_width = ""
        if target_height:
            self.target_height = int(target_height)
        else:
            self.target_height = ""
            
        try:
            actual_object = self.model_object.resolve(context)
            # check object.fieldname is an instance of a ImageWithHighlightField.
            
            field_name = actual_object.field.name
            instance = actual_object.instance
            
            try:            
                im_width = actual_object.width
                im_height = actual_object.height
            except IOError, e:
                raise ImageMagickOSFileError("File not found: %s" % actual_object.path)
                        
            highlight_x = getattr(instance, "%s_highlight_x" % field_name, None)
            highlight_y = getattr(instance, "%s_highlight_y" % field_name, None)
            highlight_width = getattr(instance, "%s_highlight_width" % field_name, None)
            highlight_height = getattr(instance, "%s_highlight_height" % field_name, None)
                        
            try:
                # if they are all present then we should be able to add them together, if there's a None in there then this will raise a TypeError
                all_ints = highlight_x + highlight_y + highlight_width + highlight_height
                
                if self.target_width and self.target_height:
                    
                    # print "cropping %sx%s image to %sx%s (highlight is (%s,%s)->(%s,%s))" % (
                    #     im_width, im_height,
                    #     self.target_width, self.target_height,
                    #     highlight_x,
                    #     highlight_y,
                    #     highlight_width,
                    #     highlight_height
                    # )

                    
                    target_ratio = self.target_width*1.0/self.target_height
                    highlight_ratio = highlight_width*1.0/highlight_height
                    
                    if target_ratio > highlight_ratio: #crop box is fatter than highlight, so will come nearer at top+bottom
                        crop_y, crop_height = self.centred_crop(im_height, highlight_y, highlight_height, self.target_height)
                        crop_width = crop_height * target_ratio
                        crop_x, crop_width = self.centred_crop(im_width, highlight_x, highlight_width, crop_width)
                        
                    else: #crop box is taller than highlight, so will come nearer at left+right

                        crop_x, crop_width = self.centred_crop(im_width, highlight_x, highlight_width, self.target_width)
                        crop_height = crop_width * 1.0 / target_ratio                        
                        crop_y, crop_height = self.centred_crop(im_height, highlight_y, highlight_height, crop_height)
                    
                    #result will now be at the right aspect ratio. Now it just remains to resize to appropriate dims.
                    
                    argument_string = "-crop %sx%s+%s+%s -resize %sx%s^ -extent %sx%s" % (crop_width, crop_height, crop_x, crop_y, self.target_width, self.target_height, self.target_width, self.target_height)
                else:
                    #no desired width and height, just crop to the highlight region
                    argument_string = "-crop %sx%s+%s+%s" % (highlight_width, highlight_height, highlight_x, highlight_y)
                return convert_util(actual_object.name, argument_string)
            except TypeError:               
                #No cropping. Best we can do is the usual resize
                if not self.target_width and not self.target_height:
                    self.target_width = self.target_height = "100%"
                return convert_util(actual_object.name, "-gravity north -resize %sx%s^ -extent %sx%s -strip -quality 50" % (self.target_width, self.target_height, self.target_width, self.target_height,))

        except template.VariableDoesNotExist:
            pass

        return ''
            
