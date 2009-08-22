import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'', include('hateonyourjob.twits.urls')),
)

if settings.DEBUG is True:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/f4nt/python-dev/hoyj/src/hateonyourjob-trunk/hateonyourjob/media/'}),
    )
