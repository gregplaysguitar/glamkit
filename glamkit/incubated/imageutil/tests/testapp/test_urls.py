from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()


urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    url(r'^testit/', 'imageutil.tests.testapp.views.crop_images', name='testit'),
    url(r'^%s/(?P<path>.*)$' % settings.MEDIA_URL.strip("/"), 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)