from django.conf.urls.defaults import *

urlpatterns = patterns('Django3.video_lec.views',
	(r'^$', 'index'),

	(r'^course/(?P<course_id>\d+)/$', 'course_view'),
	(r'^(?P<course_id>\d+)/$', 'course_view'),

	(r'^video/(?P<video_id>\d+)/$', 'random_video_view'),
	(r'^random_video/(?P<video_id>\d+)/$', 'random_video_view'),
	(r'^course_video/(?P<video_id>\d+)/$', 'course_video_view'),
)
