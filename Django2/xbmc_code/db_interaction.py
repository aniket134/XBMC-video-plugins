import sys,os
sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/Django2/")
#Used by Django. 
sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/")
#Sets the environment variable for Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'Django2.settings'

import django
from video_lec.models import video_description

def get_link():
	video = video_description.objects.get(id=1).title
	print(video)
	return video
get_link()
