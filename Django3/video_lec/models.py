from xbmc_code import constants_plugin as CP

from django.db import models
import datetime

class organization(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, null=True)
	def __unicode__(self):
		return self.name
		
class person(models.Model):
	name = models.CharField(max_length=100)
	age = models.SmallIntegerField(null=True)
	sex = models.CharField(max_length=10, null=True)
	organization = models.ForeignKey(organization)
	def __unicode__(self):
		return self.name
	
class object(models.Model):
	title = models.CharField(max_length=200)
	type = models.CharField(max_length=30, choices=zip(CP.OBJECT_TYPE, CP.OBJECT_TYPE))
	file = models.FileField(upload_to='course_video', null=True, blank=True)
	unpack = models.BooleanField(default=False, blank=True)
	description = models.TextField(null=True, blank=True)
	th_image_1 = models.ImageField(null=True, upload_to='thumbnails', blank=True)
	th_image_2 = models.ImageField(null=True, upload_to='thumbnails', blank=True)
	th_image_3 = models.ImageField(null=True, upload_to='thumbnails', blank=True)
	th_image_4 = models.ImageField(null=True, upload_to='thumbnails', blank=True)
	local_excerpt_file = models.FileField(upload_to='excerpts', null=True, blank=True)
	excerpt_1 = models.FileField(upload_to='excerpts', null=True, blank=True)
	excerpt_2 = models.FileField(upload_to='excerpts', null=True, blank=True)
	excerpt_3 = models.FileField(upload_to='excerpts', null=True, blank=True)
	subject = models.CharField(max_length=200, choices=CP.SUBJECT_CHOICES, null=True, blank=True)
	other_subject = models.CharField(null=True, max_length=50, blank=True)
	content_type = models.CharField(null=True, max_length=50, blank=True, choices=zip(CP.CONTENT_TYPES, CP.CONTENT_TYPES))
	language = models.CharField(null=True, max_length=50, blank=True)
	other_language = models.CharField(null=True, max_length=50, blank=True)
	for_class = models.CharField(null=True, max_length=50, blank=True, choices=zip(CP.CLASSES, CP.CLASSES))
	applicable_from_age = models.CharField(null=True, max_length=50, blank=True)
	applicable_to_age = models.CharField(null=True, max_length=50, blank=True)
	media_type = models.CharField(null=True, max_length=50, blank=True)
	other_media_type = models.CharField(null=True, max_length=50, blank=True)
	video_resolution = models.CharField(null=True, max_length=10, blank=True, choices=zip(CP.VIDEO_RESOLUTION, CP.VIDEO_RESOLUTION))
	content_duration = models.CharField(null=True, max_length=50, blank=True)
	data_size = models.CharField(null=True, max_length=10, blank=True)
	content_alias = models.CharField(null=True, max_length=200, blank=True)
	date_added = models.DateTimeField(auto_now_add=True, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True, blank=True)
	content_duration_hour = models.IntegerField(null=True, max_length=50, blank=True, \
		choices=zip(CP.CONTENT_DURATION_HOUR, CP.CONTENT_DURATION_HOUR))
	content_duration_minute = models.IntegerField(null=True, max_length=50, blank=True, \
		choices=zip(CP.CONTENT_DURATION_MINUTE, CP.CONTENT_DURATION_MINUTE))
	upload_after_year = models.CharField(null=True, max_length=50, blank=True, \
		choices=zip(CP.UPLOADED_AFTER_YEAR, CP.UPLOADED_AFTER_YEAR))
	upload_after_month = models.CharField(null=True, max_length=50, blank=True, \
		choices=zip(CP.UPLOADED_AFTER_MONTH, CP.UPLOADED_AFTER_MONTH))
	upload_after_day = models.CharField(null=True, max_length=50, blank=True, \
		choices=zip(CP.UPLOADED_AFTER_DAY, CP.UPLOADED_AFTER_DAY))
	upload_before_year = models.CharField(null=True, max_length=50, blank=True, \
		choices=zip(CP.UPLOADED_BEFORE_YEAR, CP.UPLOADED_BEFORE_YEAR))
	upload_before_month = models.CharField(null=True, max_length=50, blank=True, \
		choices=zip(CP.UPLOADED_BEFORE_MONTH, CP.UPLOADED_BEFORE_MONTH))
	upload_before_day = models.CharField(null=True, max_length=50, blank=True, \
		choices=zip(CP.UPLOADED_BEFORE_DAY, CP.UPLOADED_BEFORE_DAY))
	person = models.ForeignKey(person, blank=True, null=True)
	linked_objects = models.ManyToManyField('self', through='chap_info', symmetrical=False, related_name='related_to') 
	
	def __unicode__(self):
		return self.title
	def __eq__(self, other):
		return self.title == other.title

class chap_info(models.Model):
	source_object = models.ForeignKey(object, related_name='from_object')
	target_object = models.ForeignKey(object, related_name='to_object')
	chap_no = models.CharField(max_length=10, null=True, blank=True)

