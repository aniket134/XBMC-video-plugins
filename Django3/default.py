import xbmc, xbmcgui,xbmcplugin,sys,os

USERNAME = 'sh1n0b1'
PLUGIN_NAME = 'Django3'
PLUGIN_PATH = '/home/'+ USERNAME +'/.xbmc/plugins/video/'

#Used by django to set the following environment variable
sys.path.append(PLUGIN_PATH)
sys.path.append(PLUGIN_PATH + PLUGIN_NAME + '/modules/')
#Sets the environment variable for Django.
os.environ['DJANGO_SETTINGS_MODULE'] = PLUGIN_NAME + '.settings'

#sys.path.append('usr/lib/python2.6') 
#sys.path.append('/usr/lib/python2.6/plat-linux2') 
#sys.path.append('/usr/lib/python2.6/lib-tk')
#sys.path.append('/usr/lib/python2.6/lib-old') 
#sys.path.append('/usr/lib/python2.6/lib-dynload') 
sys.path.append('/usr/lib/python2.6/dist-packages') 
#sys.path.append('/usr/lib/python2.6/dist-packages/PIL') 
#sys.path.append('/usr/lib/python2.6/dist-packages/gst-0.10') 
#sys.path.append('/usr/lib/pymodules/python2.6') 
#sys.path.append('/usr/lib/python2.6/dist-packages/gtk-2.0') 
#sys.path.append('/usr/lib/pymodules/python2.6/gtk-2.0') 
#sys.path.append('/usr/local/lib/python2.6/dist-packages')

import MySQLdb
import django
from Django3.video_lec.models import video

def get_link():
	title = video.objects.get(id=1).title
	print(title)
#	return title
get_link()

xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
