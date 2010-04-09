# Code largely from Julien's stream app
import os

from django.test import TestCase
from django.conf import settings
from django.core.management import call_command
from django.db.models.loading import load_app
from django import template
from django.template.loaders import app_directories


class ImageWithHighlightTestCase(TestCase):
    
    def setUp(self):
        # Trick to be able to use test templates (inspired from django.contrib.auth.tests.views.ChangePasswordTest)
        self.old_TEMPLATE_DIRS = settings.TEMPLATE_DIRS
        settings.TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__),'templates'),)
        
        # Trick to dynamically install a test-specific app (until ticket #7835 get checked in: http://code.djangoproject.com/ticket/7835)
        self.old_INSTALLED_APPS = settings.INSTALLED_APPS
        settings.INSTALLED_APPS = (       
            'imageutil',
            'imageutil.tests.testapp',
        )
        load_app('imageutil.tests.testapp')
        call_command('flush', verbosity=0, interactive=False)
        call_command('syncdb', verbosity=0, interactive=False)
        
        # since django's r11862 templatags_modules and app_template_dirs are cached
        # the cache is not emptied between tests
        # clear out the cache of modules to load templatetags from so it gets refreshed
        template.templatetags_modules = []
        
        # clear out the cache of app_directories to load templates from so it gets refreshed
        app_directories.app_template_dirs = []
        # reload the module to refresh the cache
        reload(app_directories)
        
        # Load test fixtures
        self.old_FIXTURE_DIRS = settings.FIXTURE_DIRS
        settings.FIXTURE_DIRS = (os.path.join(os.path.dirname(__file__), 'fixtures'),)
        call_command('loaddata', 'iwh.json', verbosity=0, interactive=False)
        
    def tearDown(self):
        settings.TEMPLATE_DIRS = self.old_TEMPLATE_DIRS
        settings.INSTALLED_APPS = self.old_INSTALLED_APPS
        settings.FIXTURE_DIRS = self.old_FIXTURE_DIRS
        