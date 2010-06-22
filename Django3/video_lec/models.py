from django.db import models
import datetime

class course(models.Model):
	name = models.CharField(max_length=100)
	grade = models.CharField(max_length=100)
	subject = models.CharField(max_length=100)
	coordinator = models.CharField(max_length=100, blank=True)
	description = models.TextField(verbose_name='Course Description', blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	date_last_modified = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.name

class course_video(models.Model):
	course_structure = models.ForeignKey(course)
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=100, blank=True, verbose_name='Course Video Descrition')
	author_name = models.CharField(max_length=100, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	file = models.FileField(upload_to='course_video')
	
	def was_published_today(self):
		return self.date_added.date() == datetime.date.today()
	was_published_today.short_descrition = 'Uploaded Today?'	
	def __unicode__(self):
		return self.title

class ObjectOrderMapField(models.Field):
	description = 'Order of an Object in the current object.'
	__metaclass__ = models.SubfieldBase;

	def __init__(self, *args, **kwargs):
		super(ObjectOrderMapField, self).__init__(*args, **kwargs)

	def get_internal_type(self):
		return 'TextField'

	def to_python(self, value):
		if isinstance(value, dict):
			return value
		if (value == None or value == ''):
			return {}
		hash = eval(value)
		return hash

	def get_db_prep_value(self, value):
		return str(hash)

class random_video(models.Model):
	title = models.CharField(max_length=200)
	subject = models.CharField(max_length=100)
	description = models.CharField(max_length=100, verbose_name='Random Video Description', blank=True)
	author_name = models.CharField(max_length=100, blank=True)
	grade_level = models.CharField(max_length=100, blank=True)
	alias = models.CharField(max_length=100, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	file = models.FileField(upload_to='random_video')
	hashtable = ObjectOrderMapField();
	
	def was_published_today(self):
		return self.date_added.date() == datetime.date.today()
	was_published_today.short_descrition = 'Uploaded Today?'	
	def __unicode__(self):
		return self.title

