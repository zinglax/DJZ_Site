from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('blobs.views',
    # Home
    url(r'^$', 'blobs', name=""),


)