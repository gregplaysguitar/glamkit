from datetime import datetime, timedelta

from django.test import TestCase
from django.conf import settings

from timed_publishing.settings import *
from timed_publishing.tests.timed_object.models import TimedObject

from django.core.management import call_command
from django.db.models.loading import load_app
from django.template.loaders import app_directories

settings_override = {
    'INSTALLED_APPS': list(settings.INSTALLED_APPS) + ['timed_publishing.tests.timed_object'],
}
    
def setUp(self):
    
    if hasattr(self, 'settings_override'):
        for (key, value) in settings_override.items():
            if hasattr(settings, key):
                setattr(self, '_old_%s' % key, getattr(settings, key)) # Back up the setting
            setattr(settings, key, value) # Override the setting

    # clear out the cache of app_directories to load templates from so it gets refreshed
    app_directories.app_template_dirs = []
    # reload the module to refresh the cache
    reload(app_directories)
        
        
    load_app('timed_publishing.tests.timed_object')
    call_command('flush', verbosity=0, interactive=False)
    call_command('syncdb', verbosity=0, interactive=False)
        
    self.old_SERVER_STATUS = settings.SERVER_STATUS
    settings.SERVER_STATUS = 'development'
    
    timed_object_1 = TimedObject.objects.create(title="one draft", status=DRAFT_STATUS)
    timed_object_1.save()
    
    timed_object_2 = TimedObject.objects.create(title="two dummy", status=DUMMY_STATUS)
    timed_object_2.save()
    
    timed_object_3 = TimedObject.objects.create(title="three published", status=PUBLISHED_STATUS)
    timed_object_3.save()
    
    timed_object_4 = TimedObject.objects.create(title="four removed", status=REMOVED_STATUS)
    timed_object_4.save()
    
    timed_object_5 = TimedObject.objects.create(title="five scheduled before no end", status=SCHEDULED_STATUS, publish_start=datetime.now()-timedelta(hours=2))
    timed_object_5.save()
    
    timed_object_6 = TimedObject.objects.create(title="six scheduled during", status=SCHEDULED_STATUS, publish_start=datetime.now()-timedelta(hours=1), publish_end=datetime.now()+timedelta(hours=1))
    timed_object_6.save()
    
    timed_object_7 = TimedObject.objects.create(title="seven scheduled after has end", status=SCHEDULED_STATUS, publish_start=datetime.now()+timedelta(hours=1), publish_end=datetime.now()+timedelta(hours=2))
    timed_object_7.save()


def tearDown(self):
    settings.SERVER_STATUS = self.old_SERVER_STATUS
    
    # Restore settings
    if hasattr(self, 'settings_override'):
        for (key, value) in settings_override.items():
            if hasattr(self, '_old_%s' % key):
                setattr(settings, key, getattr(self, '_old_%s' % key))    
        
def test_development():
    """
    if it's a development server, do you return everything except not scheduled now?
    """
    
    all_objects = TimedObject.objects.all().values_list('title', flat=True)
    assert list(all_objects) == [u'one draft', u'two dummy', u'three published', u'four removed', u'five scheduled before no end', u'six scheduled during']
    

def test_production():
    """
    if it's a production server, do you return the right things?
    """
    settings.SERVER_STATUS = 'production'
    all_objects = TimedObject.objects.all().values_list('title', flat=True)
    
    assert list(all_objects) == [u'three published', u'five scheduled before no end', u'six scheduled during']
    
    
def test_dates():
    """
    when adding a scheduled object, you must have a start and end date.
    the end date has to be on or after the start date.
    """
    
    try:
        timed_object_date = TimedObject.objects.create(
                                    title="scheduled with no dates",
                                    status=SCHEDULED_STATUS,
                            )
        timed_object_date.full_clean()
    except Exception as inst:
            assert inst.message_dict.values()[0][0] == u'Sorry, there must be an start date.'
            
    try:
        timed_object_date = TimedObject.objects.create(
                                    title="scheduled with no dates",
                                    status=SCHEDULED_STATUS,
                                    publish_start=datetime(2010,1,1,0,0,0),
                                    publish_end=datetime(2009,12,31,0,0,0),
                            )
        timed_object_date.full_clean()
    except Exception as inst:
            assert inst.message_dict.values()[0][0] == u'end date (2009-12-31 00:00:00) must be greater than (or the same as) start date (2010-01-01 00:00:00).'