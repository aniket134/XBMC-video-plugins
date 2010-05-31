import xbmc, xbmcgui,xbmcplugin,sys,os,urllib

# Used to import randon stuff.
sys.path.append(os.getcwd())
# Used to import plugin specific modules.
sys.path.append(os.getcwd() + '/modules/')
# Used to import plugin related code.
sys.path.append(os.getcwd() + '/xbmc_code/')

import constants_plugin as CP
# Used by django to set DJANGO_SETTINGS_MODULE environment variable.
# See xbmc_code.db_interaction
sys.path.append(CP.PLUGIN_PATH)

import db_interaction as db
# -----------------------------------------------------------------

def ADD_DIR(name, mode, iconimage, infoLabels):
	"""
	Add a directory item in XBMC list. Note: there is no 'url' parameter in this function.
	- Returns a boolean True if successful. 

	name: int - id of the course corresponding to the list item.
	mode: int - Specifies what mode should be used when we click this link.
	iconimage: string - URL to the iconimage.
	infoLabels: hashtable - Contains info labels for this list item.
	"""
        u = sys.argv[0]+"?url=watup&mode="+str(mode)+"&name="+str(name)
	ok = True
	liz = xbmcgui.ListItem(label = infoLabels['name'], iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo(type = "Video", infoLabels = infoLabels)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def ADD_LINK(name, url, iconImage, infoLabels):
	"""
	Add a Link item in XBMC list. Note: there is no 'mode' parameter in this function.
	- Returns a boolean True if successful. 

	name: string - Title of the video.
	url: string - Specifies the url of video. It can be on disk or network.
	iconimage: string - URL to the iconimage.
	infoLabels: string - Contains info labels for this list item.
	"""
	ok = True
	liz = xbmcgui.ListItem(label = name,label2 = "",iconImage = "DefaultVideo.png",thumbnailImage = iconImage)
	liz.setInfo(type = "Video", infoLabels = infoLabels)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = url, listitem = liz)
	return ok

def add_initial_list():
	"""
	This displays the first list of items when the plugin is run.
	"""
	info_labels = {}
	info_labels['name'] = 'Search'
	ADD_DIR(0, 1, "", info_labels)
	info_labels['name'] = 'Course List'
	ADD_DIR(0, 2, "", info_labels)
	info_labels['name'] = 'Random Videos'
	ADD_DIR(0, 3, "", info_labels)

def add_course_list():
	"""
	Add all the courses present in the course table. 
	"""
	course_objects = db.get_course_objects()
	info_labels = {}
	for course in course_objects:
		info_labels = db.get_course_info_labels(course)
		ADD_DIR(course.id, 4, "", info_labels)

def add_course_videos(name):
	"""
	Add all the course related videos present in the course_video table. 
	This displays the list when a course is clicked in the first list.

	name: string - The id of course of whom the videos are being fetched.
	"""
	course_video_objects = db.get_course_video_objects(int(name))
	for video in course_video_objects:
		info_labels = db.get_course_video_info_labels(video)
		u = video.file.path
		ADD_LINK(video.title, u, "", info_labels)

def add_random_videos():
	"""
	Add all the videos present in the random_video table. 
	This displays the list when Random Videos is clicked in the first list.
	"""
	random_video_objects = db.get_random_video_objects()
	for video in random_video_objects:
		info_labels = db.get_random_video_info_labels(video)
		u = video.file.path
		ADD_LINK(video.title, u, "", info_labels)


def keyboard_search():
	keyboard = xbmc.Keyboard('Type here', 'Search')
	keyboard.doModal()
	if (keyboard.isConfirmed() == False):
		return
	searchstring = keyboard.getText()
	newStr = searchstring.replace(' ','+')
	if len(newStr) == 0:
		return
	info_labels = {'title': newStr}
	ADD_LINK(newStr, newStr, "", info_labels)
	#showList(url,newStr)


def get_params():
	"""
	Returns the parameters that were passed as a hashtable. A handy XBMC function.
	"""
	# Initialize param as empty list, could be anything
        param = []
	# Get all parameters as string
        paramstring = sys.argv[2]
	# Check the size of that string
        if len(paramstring) >= 2:
		# Get all parameters as another string
                params = sys.argv[2]
		# Delete ?, the one in the front, as other are converted in %xx format by quote_plus function
                cleanedparams = params.replace('?','')
		# Delete trailing /
                if (params[len(params)-1] == '/'):
                        params = params[0:len(params)-2]
		# Get parameter name and value as pairs
                pairsofparams = cleanedparams.split('&')
		# Initialize hashtable object to be returned
                param = {}
		# Run a loop for all parameter name-value pairs
                for i in range(len(pairsofparams)):
                        splitparams = {}
                        splitparams = pairsofparams[i].split('=')
                        if (len(splitparams)) == 2:
                                param[splitparams[0]] = splitparams[1]
        return param
# ---------------------------------------------------------

params = get_params()
name = None
mode = None
# Retrieving parameters
try:
        name = int(params["name"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass

# Deciding which way to go now
if mode == None:
	print('############### mode = None')
        add_initial_list()
       
elif mode == 1:
	print('############### mode = 1')
        keyboard_search()
        
elif mode == 2:
	print('############### mode = 2')
	add_course_list()

elif mode == 3:
	print('############### mode = 3')
        add_random_videos()
elif mode == 4:
	print('############### mode = 4')
	add_course_videos(name)




xbmcplugin.endOfDirectory(handle = int(sys.argv[1]))
