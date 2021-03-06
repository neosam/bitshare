from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bitshare.views.home', name='home'),
    # url(r'^bitshare/', include('bitshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^loading/(?P<uuid>.*)$', 'staticload.views.getLink'),
    url(r'^request/(?P<address>.*)$', 'staticload.views.request'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploadtest/$', 'staticload.views.upload'),
    url(r'^download/(?P<address>.*)$', 'staticload.views.download'),
)
