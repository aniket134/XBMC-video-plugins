from Django2.surf_videos.models import *
from django.contrib import admin

class videoAdmin(admin.ModelAdmin):
	fieldsets=[
		('Name',{'fields':['name']}),
		('Subject',{'fields':['subject']}),
		('Details',{'fields':['upload_date','rating']}),
	]
	list_display=('name','subject','upload_date','rating')
	list_filter=['upload_date']
	search_fields=['name']
	date_hierarchy='upload_date'
admin.site.register(video,videoAdmin)
