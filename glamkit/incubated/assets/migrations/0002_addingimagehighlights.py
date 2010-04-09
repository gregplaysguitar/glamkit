
from south.db import db
from django.db import models
from assets.models import *

class Migration:
    
    def forwards(self, orm):
        db.add_column('assets_image', 'file_highlight_x',  models.IntegerField(null=True, blank=True))
        db.add_column('assets_image', 'file_highlight_y',  models.IntegerField(null=True, blank=True))    
        db.add_column('assets_image', 'file_highlight_width',  models.IntegerField(null=True, blank=True))
        db.add_column('assets_image', 'file_highlight_height',  models.IntegerField(null=True, blank=True))

        db.add_column('assets_video', 'image_highlight_x',  models.IntegerField(null=True, blank=True))
        db.add_column('assets_video', 'image_highlight_y',  models.IntegerField(null=True, blank=True))    
        db.add_column('assets_video', 'image_highlight_width',  models.IntegerField(null=True, blank=True))
        db.add_column('assets_video', 'image_highlight_height',  models.IntegerField(null=True, blank=True))

    
    def backwards(self, orm):
        db.delete_column('assets_image', 'file_highlight_x')
        db.delete_column('assets_image', 'file_highlight_y')    
        db.delete_column('assets_image', 'file_highlight_width')
        db.delete_column('assets_image', 'file_highlight_height')

        db.delete_column('assets_video', 'image_highlight_x')
        db.delete_column('assets_video', 'image_highlight_y')    
        db.delete_column('assets_video', 'image_highlight_width')
        db.delete_column('assets_video', 'image_highlight_height')
    
    
    models = {
        'assets.file': {
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'})
        },
        'assets.image': {
            '_alt_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('ImageWithHighlightField', ['"Image File"'], {'height_field': '"height"', 'width_field': '"width"', 'max_length': '200'}),
            'file_highlight_height': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'file_highlight_width': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'file_highlight_x': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
            'file_highlight_y': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'visualmedia_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['assets.VisualMedia']", 'unique': 'True', 'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'assets.video': {
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            'iheight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('ImageWithHighlightField', ['"Highlight Frame"'], {'height_field': '"iheight"', 'width_field': '"iwidth"', 'max_length': '200', 'blank': 'True', 'null': 'True'}),
            'image_highlight_height': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'image_highlight_width': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'image_highlight_x': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
            'image_highlight_y': ('django.db.models.fields.IntegerField', [], {'default': '20', 'null': 'True', 'blank': 'True'}),
            'iwidth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vheight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'visualmedia_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['assets.VisualMedia']", 'unique': 'True', 'primary_key': 'True'}),
            'vwidth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'assets.visualmedia': {
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['assets']
