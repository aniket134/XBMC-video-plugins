import sys,os
#For importing django module
sys.path.append('/usr/lib/python2.6/dist-packages') 

#Used by django to set the following environment variable
sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/")
#Sets the environment variable for Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'Django3.settings'

import django
from Django3.video_lec.models import video

def get_link():
	title = video.objects.get(id=1).title
	print(title)
	return title
get_link()
