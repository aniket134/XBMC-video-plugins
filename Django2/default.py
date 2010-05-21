import xbmc,xbmcgui,xbmcplugin,sys,init_django
from xbmc_code import add_links

add_links.main()
init_django.main()

xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )
