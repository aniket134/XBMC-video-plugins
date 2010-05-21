class video(models.Model):
	name=models.CharField(max_length=200)
	subject=models.CharField(max_length=200)
	rating=models.IntegerField()
	upload_date=models.DateTimeField('Uploaded Date')
	def __unicode__(self):
		return self.name
	def was_uploaded_today(self):
		return self.upload_date.date()==datetime.date.today()
	was_uploaded_today.short_description='Uploaded Today?'
