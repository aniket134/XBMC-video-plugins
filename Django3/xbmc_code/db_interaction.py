import sys, os, django, re
import constants_plugin as CP

# Very important environment variable used by Django.
# It is set in this file because unlike sys.path it is not carried
# forward when one python script calls another python script.
# So we have to set it in every python file we have to use django DB.
# Remember, it must be set before any Django model is imported.
os.environ['DJANGO_SETTINGS_MODULE'] = CP.DJANGO_SETTINGS_MODULE

from video_lec.models import object, person, organization

#def get_course_objects():
#	course_objects = course.objects.all().order_by('-date_last_modified')[:10]
#	return course_objects
#
#def get_course_video_objects(course_id):
#	course_video_objects = course.objects.get(id = course_id).course_video_set.all()
#	return course_video_objects
#
#def get_random_video_objects():
#	random_video_objects = random_video.objects.all()
#	return random_video_objects
#
#def get_course_info_labels(c):
#	dict = {}
#	dict['name'] = c.name
#	return dict
#
#def get_course_video_info_labels(cv):
#	dict = {}
#	dict['title'] = cv.title
#	return dict
#
#def get_random_video_info_labels(rv):
#	dict = {}
#	dict['title'] = rv.title
#	return dict
#
#def search(text):
#	links = ['str', 'lkj']
#	return links
