import sys, os, django
import constants_plugin as CP

# Very important environment variable used by Django.
# It is set in this file because unlike sys.path it is not carried
# forward when one python script calls another python script.
# So we have to set it in every python file we have to use django DB.
# Remember, it must be set before any Django model is imported.
os.environ['DJANGO_SETTINGS_MODULE'] = CP.DJANGO_SETTINGS_MODULE

from video_lec.models import course, course_video, random_video

def get_course_objects():
	course_objects = course.objects.all().order_by('-date_last_modified')[:10]
	return course_objects

def get_info_labels(c):
	dict = {}
	dict['title'] = c.name
	return dict
