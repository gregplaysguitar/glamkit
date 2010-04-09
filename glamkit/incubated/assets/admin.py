from django.contrib import admin
from django import forms
from django.shortcuts import get_object_or_404

from imageutil.model_fields import IMAGE_WITH_HIGHLIGHT_ADMIN
from ixc_common.widgets import MarkItUpWidget

from widgets import FloatedSelectMultiple
from models import *
from tree_structure_admin import TreeNodeAdminMixIn
from tree_structure_models import TreeNodeMixIn

        
# class VideoAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=MarkItUpWidget(), required=False, help_text='Use <a href="http://daringfireball.net/projects/markdown/syntax" target="_blank">Markdown Syntax</a> for this part.')
# 
#     class Meta:
#         model = Video

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'extension', 'link', 'publish_date', 'size')
    date_hierarchy = "publish_date"
    exclude = ('mime_type',)
    fieldsets = (
        (None, {'fields': ('file', '_name', 'publish_date',)}),
    )

class ImageAdmin(admin.ModelAdmin):
    list_display = ('name','just_thumb','highlight_thumb', 'dimensions_text', 'aspect_ratio', 'alt_text',)
    exclude = ('mime_type',)
    fieldsets = (
        IMAGE_WITH_HIGHLIGHT_ADMIN('file'),
        (None, {'fields': ('_name', '_alt_text',)}),
    )
    ordering = ("file",)
    

class VideoAdmin(admin.ModelAdmin):
    list_display = ('name','thumb','dimensions_text','size')
    exclude = ('mime_type',)
    fieldsets = (
        (None, {'fields': ('file', '_name', 'image', 'vwidth', 'vheight')}),
    )
    ordering = ("_name", "file")

    # form = VideoAdminForm

admin.site.register(File, FileAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Video, VideoAdmin)