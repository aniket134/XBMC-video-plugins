import xbmc, xbmcgui, xbmcplugin, sys, os, urllib

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

def get_links(search_text):
	links = []
	links.append(search_text)
	links.append(search_text + 'a')
	return links
