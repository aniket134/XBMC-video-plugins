from django.db import models
import datetime

class video(models.Model):
	title = models.CharField(max_length=200)
	subject = models.CharField(max_length=100)
	description = models.CharField(max_length=100)
	author_name = models.CharField(max_length=100)
	grade_level = models.CharField(max_length=100)
	alias = models.CharField(max_length=100)
	date_uploaded = models.DateTimeField('date_uploaded')

	def was_published_today(self):
		return self.date_uploaded.date() == datetime.date.today()
	was_published_today.short_descrition = 'Uploaded Today?'	
	def __unicode__(self):
		return self.title
