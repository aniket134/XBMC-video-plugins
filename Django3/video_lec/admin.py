from xbmc_code import constants_plugin as CP
PN = __import__(CP.PLUGIN_NAME)
chap_info = PN.video_lec.models.chap_info
object = PN.video_lec.models.object
person = PN.video_lec.models.person
organization = PN.video_lec.models.organization

from django.contrib import admin
from django.forms import ModelForm
from django import forms
	
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

class ObjectInline(admin.StackedInline):
	model = chap_info
	fk_name = "target_object"
	extra = 3
	
class ObjectForm(ModelForm):
	class Meta:
		model = object
	#subject = forms.MultipleChoiceField(choices=SUBJECT_CHOICES, widget=forms.CheckboxSelectMultiple())
	#def clean_subject(self):
	#	list = self.cleaned_data['subject']
	#	return self.cleaned_data['subject']


class ObjectAdmin(admin.ModelAdmin):
	form = ObjectForm
	inlines = (ObjectInline,)

admin.site.register(chap_info)
admin.site.register(object, ObjectAdmin)
admin.site.register(person)
admin.site.register(organization)
