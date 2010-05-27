from django.db import models

# Create your models here.
class video_description(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=500)
	author = models.CharField(max_length=50)
	subject = models.CharField(max_length=50)
	grade_level = models.CharField(max_length=50)
	date_uploaded = models.DateTimeField()
	topic = models.CharField(max_length=100)
	def __unicode__(self):
		return self.title
