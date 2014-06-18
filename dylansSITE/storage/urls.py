from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('storage.views',
    url(r'^$', 'storage', name=""),
    url(r'^add', 'add',name='add'),
    url(r'^search', 'search',name='search'),
    
)