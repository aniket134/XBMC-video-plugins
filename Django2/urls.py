from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #(r'^surf_videos/$','Django2.surf_videos.views.index'),
    #(r'^surf_videos/(?P<vid_id>\d+)/$','Django2.surf_videos.views.detail'),
    #(r'^surf_videos/(?P<vid_id>\d+)/results/$','Django2.surf_videos.views.results'),
    #(r'^surf_videos/(?P<vid_id>\d+)/rating/$','Django2.surf_videos.views.rating'),
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
