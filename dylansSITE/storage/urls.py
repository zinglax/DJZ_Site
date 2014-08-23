from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('storage.views',
    url(r'^$', 'storage', name=""),
    url(r'^add/(?P<bar_code>DJZ\d+)/$', 'add',name='add'),
    url(r'^search', 'search',name='search'),
    url(r'^(?P<bar_code>DJZ\d+)/$', 'item', name='item'),
)