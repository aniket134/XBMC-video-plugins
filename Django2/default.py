import xbmc,xbmcgui,xbmcplugin,sys
sys.path.append("/usr/lib/python2.6/")
import django,init_django
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

addDir("folder1", "/home/sh1n0b1/.xbmc/plugins/Django2/",1,"")
addLink("DSH Video 1","/home/sh1n0b1/Downloads/Videos/0326shashi2_withtext.avi","")

init_django.main()
xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
