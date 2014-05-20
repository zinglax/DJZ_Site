from django.conf.urls import *
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djz_site.views.home', name='home'),
    # url(r'^djz_site/', include('djz_site.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    url(r'^resume/', 'resume.views.resume', name='resume'),
    
    # Nav using number keys 1 2 3 4 5
    #url(r'^quickNav/(\d+)', 'quickNav.views.quickNav', name='quickNav'),
)
