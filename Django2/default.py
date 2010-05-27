import xbmc,xbmcgui,xbmcplugin,sys,os,django,init_django
from pysqlite2 import dbapi2

#from xbmc_code import add_links

#Used by Django. 
sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/")

sys.path.append('usr/lib/python2.6') 
sys.path.append('/usr/lib/python2.6/plat-linux2') 
sys.path.append('/usr/lib/python2.6/lib-tk')
sys.path.append('/usr/lib/python2.6/lib-old') 
sys.path.append('/usr/lib/python2.6/lib-dynload') 
sys.path.append('/usr/lib/python2.6/dist-packages') 
sys.path.append('/usr/lib/python2.6/dist-packages/PIL') 
sys.path.append('/usr/lib/python2.6/dist-packages/gst-0.10') 
sys.path.append('/usr/lib/pymodules/python2.6') 
sys.path.append('/usr/lib/python2.6/dist-packages/gtk-2.0') 
sys.path.append('/usr/lib/pymodules/python2.6/gtk-2.0') 
sys.path.append('/usr/local/lib/python2.6/dist-packages')
sys.path.append("/home/sh1n0b1/.xbmc/plugins/video/Django2/")
#Sets the environment variable for Django.
os.environ['DJANGO_SETTINGS_MODULE'] = 'Django2.settings'
import MySQLdb

#conn = dbapi2.connect('sampledb.db')
#curs = conn.cursor()
#curs.close()
#conn.close()
#add_links.main()
#init_django.main()

xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
