import xbmc, xbmcgui,xbmcplugin,sys,os,urllib

# Used to import django plugins and make plugin name irrelevant
sys.path.append(os.getcwd())
# Used to import plugin specific modules
sys.path.append(os.getcwd() + '/modules/')
# Used to import plugin related code
sys.path.append(os.getcwd() + '/xbmc_code/')

import constants_plugin as CP
# Used by django to set DJANGO_SETTINGS_MODULE environment variable.
# See xbmc_code.db_interaction
sys.path.append(CP.PLUGIN_PATH)

import db_interaction as db

def addDir(name, url, mode, iconimage, infoLabels):
	"""
	Add a directory item in XBMC list. Returns a boolean True if successful.
	"""
	ok=True
	liz=xbmcgui.ListItem(label=name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo(type="Video", infoLabels=infoLabels)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz, isFolder=True)
	return ok

def addLink(name, url, iconImage, infoLabels):
	"""
	Add a Link item in XBMC list. Returns a boolean True if successful.
	"""
	ok=True
	liz=xbmcgui.ListItem(label=name,label2="",iconImage="DefaultVideo.png",thumbnailImage=iconImage)
	liz.setInfo(type="Video", infoLabels=infoLabels)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz)
	return ok

course_objects = db.get_course_objects()
for course in course_objects:
	info_labels = db.get_info_labels(course)
	addDir(course.name, os.getcwd(), 1, "", info_labels)







xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
