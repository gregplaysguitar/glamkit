from django.conf.urls.defaults import *

# Regular views
urlpatterns = patterns('assets.views',
    url(r'^$', 'file_index'),
)
