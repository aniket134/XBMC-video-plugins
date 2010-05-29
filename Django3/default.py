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


addDir(db.get_link(), os.getcwd(),1,"")
xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
