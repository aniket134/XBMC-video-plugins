from Django3.video_lec.models import video
from django.contrib import admin

class VideoAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['title']}),
		('Video Information', {'fields': ['subject', 'description', 'author_name', 'grade_level', 'alias', 'date_uploaded'], 'classes': ['collapse']}),
	]

	list_display = ('subject', 'author_name', 'was_published_today')

	list_filter = ['date_uploaded', 'title']
	search_fields = ['title', 'author']
	#date_hierarchy = 'date_uploaded'

admin.site.register(video, VideoAdmin)
