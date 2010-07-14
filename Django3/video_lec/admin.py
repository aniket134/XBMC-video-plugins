from xbmc_code import constants_plugin as CP
PN = __import__(CP.PLUGIN_NAME)
chap_info = PN.video_lec.models.chap_info
object = PN.video_lec.models.object
person = PN.video_lec.models.person
organization = PN.video_lec.models.organization

from django.contrib import admin
from django.forms import ModelForm
from django import forms
	
class ObjectInline(admin.StackedInline):
	model = chap_info
	fk_name = "target_object"
	extra = 3
	
class ObjectForm(ModelForm):
	class Meta:
		model = object
#	subject = forms.MultipleChoiceField(choices=SUBJECT_CHOICES, widget=forms.CheckboxSelectMultiple())
#	def clean_subject(self):
#		list = self.cleaned_data['subject']
#		return self.cleaned_data['subject']


class ObjectAdmin(admin.ModelAdmin):
	form = ObjectForm
	inlines = (ObjectInline,)

admin.site.register(chap_info)
admin.site.register(object, ObjectAdmin)
admin.site.register(person)
admin.site.register(organization)
