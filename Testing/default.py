import xbmc,xbmcgui,xbmcplugin,urllib,os

def getRoots():
	if(os.name == "posix"):
		addDir("Root","/",1,"")
	elif(os.name == "nt"):
		for i in range(ord('a'), ord('z')+1):
			drive = chr(i) + ":\\"
			if os.path.exists(drive):
				addDir(drive,drive,1,"")
def addDir(name,url,mode,iconimage):
	u=url
	ok=True
	liz=xbmcgui.ListItem(label=name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	xbmc.log("asdf"+sys.argv[0]+"--"+sys.argv[1]+"--"+sys.argv[2])
	xbmc.log("zxcv:::"+u)
	return ok

def addLink(name,url,iconImage):
	ok=True
	liz=xbmcgui.ListItem(label=name,label2="",iconImage="DefaultVideo.png",thumbnailImage=iconImage)
	liz.setInfo(type="Video",infoLabels={"Title":name})
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

getRoots()
addDir("folder1", "C:/Users/Aniket/AppData/Roaming/XBMC/plugins/Video/Testing/folder1/",1,"")

xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )