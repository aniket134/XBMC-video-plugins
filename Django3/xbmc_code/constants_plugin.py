"""
 This file contains some constants used by the plugin. 
 Use caution while modifying this file and changing its location. 
"""
import sys,os
#: The username of Ubuntu user for whom this plugin is developed. Be carefull, it can be root if XBMC is run with sudo command.
USERNAME = os.getenv('USERNAME')

cwd = os.getcwd()
spls =  cwd.split('/')

#: The name of plugin and also the name of Django project
PLUGIN_NAME = spls.pop(len(spls)-1)
# We need to pop only once, as this script is run from Django3 directory... Don't know why or how
PLUGIN_PATH = '/'

#: The path to all XBMC video plugins and more importantly it is the path to Django's projects. Used for DJANGO_SETTINGS_MODULE.
PLUGIN_PATH = PLUGIN_PATH.join(spls)

print(PLUGIN_NAME)
print(PLUGIN_PATH)
print(USERNAME)
#: The environment variable which is used by Django to figure out the for which project it is being used.
DJANGO_SETTINGS_MODULE = PLUGIN_NAME + '.settings'
