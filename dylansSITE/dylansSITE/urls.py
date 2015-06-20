from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', include('dylansSITE.home.urls')),
    url(r'^$', 'home.views.home', name='home'),
    #url(r'^mobilewebpractice', 'home.views.mobilewebpractice',name='mobilewebpractice'),
    #url(r'^resume', 'home.views.resume',name='resume'),
    url(r'^images', 'home.views.images',name='images'),
    url(r'^storage/', include('storage.urls')),
    #url(r'^blobs/', include('blobs.urls')),
    
    url(r'^photobooth', 'home.views.photobooth',name='photobooth'),
    url(r'^voice', 'home.views.voice',name='voice'),
    
    url(r'^register/$', 'home.views.register', name='register'),
    url(r'^login/$', 'home.views.user_login', name='login'),    
    url(r'^restricted/', 'home.views.restricted', name='restricted'),
    url(r'^logout/$', 'home.views.user_logout', name='logout'),

    # Payments
    url(r'^payments/$', 'home.views.payments', name='payments'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'home.views.custom_404'
handler500 = 'home.views.custom_500'