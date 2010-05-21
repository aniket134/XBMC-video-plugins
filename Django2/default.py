import xbmc,xbmcgui,xbmcplugin,sys,os,django,sqlite3_for_xbmc

from xbmc_code import add_links
import init_django

sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/Django2/")
#Used by Django. 
sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/")
#Sets the environment variable for Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'Django2.settings'

add_links.main()
init_django.main()

xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
