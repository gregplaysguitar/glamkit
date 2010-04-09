
from south.db import db
from django.db import models
from assets.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Video'
        db.create_table('assets_video', (
            ('visualmedia_ptr', orm['assets.Video:visualmedia_ptr']),
            ('file', orm['assets.Video:file']),
            ('image', orm['assets.Video:image']),
            ('vwidth', orm['assets.Video:vwidth']),
            ('vheight', orm['assets.Video:vheight']),
            ('iwidth', orm['assets.Video:iwidth']),
            ('iheight', orm['assets.Video:iheight']),
        ))
        db.send_create_signal('assets', ['Video'])
        
        # Adding model 'File'
        db.create_table('assets_file', (
            ('id', orm['assets.File:id']),
            ('_name', orm['assets.File:_name']),
            ('mime_type', orm['assets.File:mime_type']),
            ('file', orm['assets.File:file']),
            ('publish_date', orm['assets.File:publish_date']),
        ))
        db.send_create_signal('assets', ['File'])
        
        # Adding model 'Image'
        db.create_table('assets_image', (
            ('visualmedia_ptr', orm['assets.Image:visualmedia_ptr']),
            ('file', orm['assets.Image:file']),
            ('_alt_text', orm['assets.Image:_alt_text']),
            ('width', orm['assets.Image:width']),
            ('height', orm['assets.Image:height']),
        ))
        db.send_create_signal('assets', ['Image'])
        
        # Adding model 'VisualMedia'
        db.create_table('assets_visualmedia', (
            ('id', orm['assets.VisualMedia:id']),
            ('_name', orm['assets.VisualMedia:_name']),
            ('mime_type', orm['assets.VisualMedia:mime_type']),
        ))
        db.send_create_signal('assets', ['VisualMedia'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Video'
        db.delete_table('assets_video')
        
        # Deleting model 'File'
        db.delete_table('assets_file')
        
        # Deleting model 'Image'
        db.delete_table('assets_image')
        
        # Deleting model 'VisualMedia'
        db.delete_table('assets_visualmedia')
        
    
    
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
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '200'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'visualmedia_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['assets.VisualMedia']", 'unique': 'True', 'primary_key': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'assets.video': {
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '200'}),
            'iheight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
