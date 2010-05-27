
"""
 This file contains some constants used by the plugin. 
 Use caution while modifying them.
"""

#: The username of Ubuntu user for whom this plugin is developed.
USERNAME = 'sh1n0b1'

PLUGIN_NAME = 'Django3'#: The name of plugin and also the name of Django project

#: The path to all XBMC video plugins and more importantly it is the path to Django's projects. Used for DJANGO_SETTINGS_MODULE.
PLUGIN_PATH = '/home/'+ USERNAME +'/.xbmc/plugins/video/'

#: The environment variable which is used by Django to figure out the for which project it is being used.
DJANGO_SETTINGS_MODULE = PLUGIN_NAME + '.settings'
