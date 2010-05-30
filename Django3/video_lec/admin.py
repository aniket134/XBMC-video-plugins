from xbmc_code import constants_plugin as CP
PN = __import__(CP.PLUGIN_NAME)
course = PN.video_lec.models.course
course_video = PN.video_lec.models.course_video
random_video = PN.video_lec.models.random_video

from django.contrib import admin

class CourseVideoInline(admin.StackedInline):
	model = course_video
	extra = 3

class CourseAdmin(admin.ModelAdmin):
	list_display = ('name', 'grade', 'subject', 'date_last_modified', 'date_added')
	inlines = [CourseVideoInline]

#This is not being used currently
class CourseVideoAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['course', 'title']}),
		('Video Information', {'fields': ['description', 'author_name', 'date_added'], 'classes': ['collapse']}),
	]
	list_display = ('title', 'course', 'author_name', 'was_published_today')
	
	list_filter = ['date_added', 'title']
	search_fields = ['title', 'author']

class RandomVideoAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields': ['title', 'subject']}),
		('Video Information', {'fields': ['file', 'description', 'author_name', 'grade_level', 'alias'], 'classes': ['collapse']}),
	]
	list_display = ('title', 'subject', 'author_name', 'was_published_today', 'date_added')
	list_filter = ['date_added', 'title']
	search_fields = ['title', 'author']
	#date_hierarchy = 'date_added'

#admin.site.register(course_video, CourseVideoAdmin)
admin.site.register(course, CourseAdmin)
admin.site.register(random_video, RandomVideoAdmin)
