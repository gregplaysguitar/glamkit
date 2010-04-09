from django.conf.urls.defaults import *

urlpatterns = patterns('tellafriend.views',
    # need to wrap up this generic view inside a decorator or something 
    url(r'^$', 'tellafriend', name='tellafriend'),
    url(r'^message_sent/$', 'message_sent', name='message_sent'),
    url(r'^(?P<theme>[\w-]+)/$', 'tellafriend', name='tellafriend'),
)