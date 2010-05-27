from django.db import models

class video(models.Model):
	title = models.CharField(max_length=200)
	subject = models.CharField(max_length=100)
