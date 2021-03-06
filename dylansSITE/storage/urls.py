from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('storage.views',
    # Home
    url(r'^$', 'storage', name=""),

    # Add
    url(r'^add/(?P<bar_code>DJZ\d+)/$', 'add',name='add'),

    # Search
    url(r'^search', 'search',name='search'),
    
    # Update
    url(r'^update', 'update',name='update'),    
    url(r'^u/(?P<bar_code>DJZ\d+)/', 'update_item',name='update_item'),    

    # Item
    url(r'^(?P<bar_code>DJZ\d+)/$', 'item', name='item'),
    
    # Export Database
    url(r'^export', 'export', name='export'),
    
    # About
    url(r'^about', 'about', name='about'),
    
)