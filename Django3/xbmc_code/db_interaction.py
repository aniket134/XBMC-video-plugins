import sys,os
import constants_plugin as CP

# Very important environment variable used by Django.
# It is set in this file because unlike sys.path it is not carried
# forward from one python script to scriipt.
# So we have to set it in any python file we have to use django DB.
# It has to be set before any Django model is imported
os.environ['DJANGO_SETTINGS_MODULE'] = CP.DJANGO_SETTINGS_MODULE

import django
from Django3.video_lec.models import video

def get_link():
	title = video.objects.get(id=1).title
	return title
