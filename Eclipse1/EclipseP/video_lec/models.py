from django.db import models
import datetime


class organization(models.Model):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=100, null=True)
		
class person(models.Model):
	name = models.CharField(max_length=100)
	age = models.SmallIntegerField(null=True)
	sex = models.CharField(max_length=10, null=True)
	organization = models.ForeignKey(organization)
	
SUBJECT_CHOICES = (
				('ENG', 'English'),
				('HIN', 'Hindi'),
				('SAN', 'Sanskrit'),
				('SCI', 'Science'),
				('PHY', 'Physics'),
				('CHY', 'Chemistry'),
				('AST', 'Astronomy'),
				('BIO', 'Biology'),
				('GEO', 'Geology'),
				('MAT', 'Mathematics'),
				('ART', 'Arithmetic'),
				('ALG', 'Algebra'),
				('GMT', 'Geometry'),
				('HIS', 'History'),
				('SST', 'Social Studies'),
				('HSC', 'Home Science'),
				('AGR', 'Agriculture'),
				('COM', 'Commerce'),
				('CAC', 'Culture and Customs'),
				('GKN', 'General Knowledge'),
				('FAN', 'Food and Nutrition'),
				('AAC', 'Arts and Crafts'),
				('CLY', 'Computer Literacy'),
				('GAM', 'Games'),
				('STR', 'Stories'),
				('PLY', 'Plays'),
				('VOC', 'Vocabulary'),
				('ENV', 'Environmental Science'),
				('HCR', 'Health Care'),
				('NUR', 'Nursing'),
				('RPH', 'Reproductive Health'),
				('CHH', 'Children Health'),
				('WRT', 'Women Rights'),
				('KAN', 'Kannada'),
				('TAM', 'Tamil'),
				('BEN', 'Bengali'),
				('MAR', 'Marathi'),
				('PUN', 'Punjabi'),
				('URD', 'Urdu'),
				('NEP', 'Nepali'),
				('CPR', 'Children Program'),
				)

class object(models.Model):
	title = models.CharField(max_length=200)
	type = models.CharField(max_length=30)
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
	subject = models.CharField(max_length=200, choices=SUBJECT_CHOICES, null=True, blank=True)
	other_subject = models.CharField(null=True, max_length=50, blank=True)
	content_type = models.CharField(null=True, max_length=50, blank=True)
	language = models.CharField(null=True, max_length=50, blank=True)
	for_class = models.CharField(null=True, max_length=50, blank=True)
	applicable_from_age = models.CharField(null=True, max_length=50, blank=True)
	applicable_to_age = models.CharField(null=True, max_length=50, blank=True)
	media_type = models.CharField(null=True, max_length=50, blank=True)
	other_media_type = models.CharField(null=True, max_length=50, blank=True)
	video_resolution = models.CharField(null=True, max_length=10, blank=True)
	content_duration = models.CharField(null=True, max_length=50, blank=True)
	data_size = models.CharField(null=True, max_length=10, blank=True)
	content_alias = models.CharField(null=True, max_length=200, blank=True)
	date_added = models.DateTimeField(auto_now_add=True, blank=True)
	date_last_modified = models.DateTimeField(auto_now=True, blank=True)
	person = models.ForeignKey(person, blank=True, null=True)
	linked_objects = models.ManyToManyField('self', through='chap_info', symmetrical=False, related_name='related_to') 
	
	def __unicode__(self):
		return self.title

class chap_info(models.Model):
	source_object = models.ForeignKey(object, related_name='from_object')
	target_object = models.ForeignKey(object, related_name='to_object')
	chap_no = models.CharField(max_length=10, null=True, blank=True)

