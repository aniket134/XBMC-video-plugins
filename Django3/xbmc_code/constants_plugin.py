"""
 This file contains some constants used by the plugin. 
 Use caution while modifying this file and changing its location. 
"""
import sys, os
#: The username of Ubuntu user for whom this plugin is developed. Be carefull, it can be root if XBMC is run with sudo command.
USERNAME = os.getenv('USERNAME')

cwd = os.getcwd()
spls =  cwd.split('/')

#: The name of plugin and also the name of Django project
PLUGIN_NAME = spls.pop(len(spls)-1)
# We need to pop only once, as this script is run from plugin home directory... Don't know why or how. Weird thing is this works for both Django and XBMC!
PLUGIN_PATH = '/'

#: The path to all XBMC video plugins and more importantly it is the path to Django's projects. Used for DJANGO_SETTINGS_MODULE. There is no '/' at the end.
PLUGIN_PATH = PLUGIN_PATH.join(spls)

#: The environment variable which is used by Django to figure out the for which project it is being used.
DJANGO_SETTINGS_MODULE = PLUGIN_NAME + '.settings'

#: Path for XBMC resources. Note the trailing slash.
RESOURCE_PATH = PLUGIN_PATH + '/' + PLUGIN_NAME + '/' + 'resources/'

#: The path where all videos are stored. Link to the videos relative to this path is stored in DB. Absolute path and trailing slash.
MEDIA_ROOT = '/media/OS/MOVIES/TV-SERIES/django_upload/'

#: Delimiter used while searching.
SEARCH_DELIMITER = '::'

SUBJECT_CHOICES = [
				('English', 'English'),
				('Hindi', 'Hindi'),
				('Sanskrit', 'Sanskrit'),
				('Science', 'Science'),
				('Physics', 'Physics'),
				('Chemistry', 'Chemistry'),
				('Astronomy', 'Astronomy'),
				('Biology', 'Biology'),
				('Geology', 'Geology'),
				('Mathematics', 'Mathematics'),
				('Arithmetic', 'Arithmetic'),
				('Algebra', 'Algebra'),
				('Geometry', 'Geometry'),
				('History', 'History'),
				('Social Studies', 'Social Studies'),
				('Home Science', 'Home Science'),
				('Agriculture', 'Agriculture'),
				('Commerce', 'Commerce'),
				('Culture and Customs', 'Culture and Customs'),
				('General Knowledge', 'General Knowledge'),
				('Food and Nutrition', 'Food and Nutrition'),
				('Arts and Crafts', 'Arts and Crafts'),
				('Computer Literacy', 'Computer Literacy'),
				('Games', 'Games'),
				('Stories', 'Stories'),
				('Plays', 'Plays'),
				('Vocabulary', 'Vocabulary'),
				('Environmental Science', 'Environmental Science'),
				('Health Care', 'Health Care'),
				('Nursing', 'Nursing'),
				('Reproductive Health', 'Reproductive Health'),
				('Children Health', 'Children Health'),
				('Women Rights', 'Women Rights'),
				('Kannada', 'Kannada'),
				('Tamil', 'Tamil'),
				('Bengali', 'Bengali'),
				('Marathi', 'Marathi'),
				('Punjabi', 'Punjabi'),
				('Urdu', 'Urdu'),
				('Nepali', 'Nepali'),
				('Children Program', 'Children Program'),
				]
MEDIA_TYPE = [
		('Video', 'Video'),
		('DVD', 'DVD'),
		('VCD', 'VCD'),
		('Extracted By Firewire', 'Extracted By Firewire'),
		('Recorded by Plextor', 'Recorded by Plextor'),
		('Recorded from TV', 'Recorded from TV'),
		('VHS', 'VHS'),
		('Tape Digitized', 'Tape Digitized'),
		('Recorded by Mustek', 'Recorded by Mustek'),
		('Recorded by Aiptek', 'Recorded by Aiptek'),
		('Recorded by CamStudio', 'Recorded by CamStudio'),
		('Created by ProShow', 'Created by ProShow'),
		('Has Subtitle', 'Has Subtitle'),
		('SMIL', 'SMIL'),
		('Audi (without video)', 'Audi (without video)'),
		('Flash', 'Flash'),
		('Images', 'Images'),
		('Powerpoint', 'Powerpoint'),
		('Documents', 'Documents'),
		('Executables', 'Executables'),
		('Slideshows', 'Slideshows'),
		]
LANGUAGES = [
		('English', 'English'),
		('Hindi', 'Hindi'),
		('Kannada', 'Kannada'),
		('Tamil', 'Tamil'),
		('Bengali', 'Bengali'),
		('Marathi', 'Marathi'),
		('Punjabi', 'Punjabi'),
		('Telegu', 'Telegu'),
		('Gujarati', 'Gujarati'),
		('Kashmiri', 'Kashmiri'),
		]
