from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('storage.views',
    url(r'^$', 'home', name='home'),
)